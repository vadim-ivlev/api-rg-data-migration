package main

import (
	"database/sql"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

// Ия файла базы данных
var dbFileName = `rg.db`

// Конечная точка API для получения текста материала. См. https://works.rg.ru/project/docs/?section=8
var urlArticle = "https://outer.rg.ru/plain/proxy/?query=https://rg.ru/api/get/object/article-%v.json"

// Таймаут запросов к API
var requestTimeout = 30

func main() {
	// считать параметры командной строки
	// batchSize Количество одновременных запросов к API.
	// status Значение поля migration_status, записей подлежащих обновлению.
	// showTiming Показывать времена исполнения
	batchSize, status, createTable, showTiming := readCommandLineParams()
	fmt.Println("showTiming=", showTiming)
	if createTable {
		// Порождаем таблицу articles
		createArticlesTable()
		// Заполняем ее пустыми записями с идентификаторами из таблицы связей rubrics_articles
		fillArticlesWithIds()
	}
	// Заполняем таблицу articles текстами из API
	fillArticlesWithTexts(batchSize, status, showTiming)

	fmt.Println("DONE")
}

// readCommandLineParams читает параметры командной строки
func readCommandLineParams() (batchSize int, status string, createTable bool, showTiming bool) {
	flag.IntVar(&batchSize, "batchSize", 50, "Количество запросов выполняемых одновременно")
	flag.StringVar(&status, "status", "", "Значение поля migration_status обновляемых записей")
	flag.BoolVar(&createTable, "createTable", false, "Создать таблицу и заполнить ее идентификаторами.")
	flag.BoolVar(&showTiming, "showTiming", false, "Показывать времена исполнения")

	flag.Parse()
	// fmt.Println("\nПример запуска: ./auth-proxy -serve 4400 -env=dev\n ")
	flag.Usage()
	if batchSize == 0 {
		os.Exit(0)
	}
	return
}

// Порождает таблицу articles в базе данных
func createArticlesTable() {
	sqlCreateArticles := `
	CREATE TABLE IF NOT EXISTS articles(
		obj_id TEXT PRIMARY KEY,
		announce TEXT,
		authors TEXT,
		date_modified TEXT, 
		"full-text" TEXT,
		images TEXT,
		index_priority TEXT,
		is_active TEXT,
		is_announce TEXT,
		is_paid TEXT,
		link_title TEXT,
		links TEXT, 
		obj_kind TEXT,
		projects TEXT,
		release_date TEXT,
		spiegel TEXT,
		title TEXT,
		uannounce TEXT,
		url TEXT,
		migration_status TEXT DEFAULT ''
	)
	`
	sqlCreateIndex := `CREATE INDEX IF NOT EXISTS articles_migration_status_idx ON articles (migration_status)`

	exec(sqlCreateArticles)
	fmt.Println("Articles table created")
	exec(sqlCreateIndex)
	fmt.Println("Indexes for articles table created")
}

// Заполняет таблицу articles идентификаторами статей полученными
// из таблицы связей rubrics_objects
func fillArticlesWithIds() {
	sqlFillArticlesWithIds := `
	INSERT OR IGNORE INTO articles
	SELECT DISTINCT 
	object_id, NULL, NULL, NULL, NULL, NULL, 
	NULL, NULL, NULL, NULL, NULL, NULL, NULL, 
	NULL, NULL, NULL, NULL, NULL, NULL, ""
	FROM rubrics_objects 
	WHERE kind = 'article'
	`
	exec(sqlFillArticlesWithIds)
	fmt.Println("Articles table is filled with ids")
}

// Заполняет таблицу articles текстами из API.
// batchSize Количество одновременных запросов к API.
// status Значение поля migration_status, записей подлежащих обновлению.
// showTiming Показывать времена исполнения
func fillArticlesWithTexts(batchSize int, status string, showTiming bool) {
	// время отдыха между порциями запросов
	var sleepTime = 50 * time.Millisecond
	// Счетчик сделанных запросов
	counter := 0
	//Время начала процесса
	startTime := time.Now()

	//Берем первую порцию идентификаторов из таблицы articles
	ids := getArticleIds(batchSize, status, showTiming)
	// Пока в порции в порции есть идентификаторы
	for len(ids) > 0 {
		//Запрашиваем тексты статей
		articleTexts := getAPITextsParallel(ids, showTiming)
		// преобразовываем тексты в записи - массивы полей материала
		articleRecords := textsToArticleRecords(articleTexts)
		// Сохраняем записи в базу данных
		saveArticlesToDatabase(articleRecords, showTiming)

		// Выводим сообщение
		counter += len(ids)
		duration := time.Since(startTime)
		durationHours := float64(duration) / float64(time.Hour)
		articlesPerHour := float64(counter) / durationHours
		fmt.Printf("Migrated total %8d articles in %v. Average migration rate = %.0f per hour. \n", counter, duration, articlesPerHour)

		// отдыхаем
		time.Sleep(sleepTime)
		// Берем следующую порцию идентификаторов
		ids = getArticleIds(batchSize, status, showTiming)
	}

}

// Получает массив идентификаторов (размером не более limit) статей из базы данных,
// в которых поле migration_status имеет значение статус.
func getArticleIds(limit int, status string, showTiming bool) []string {
	startTime := time.Now()
	db, err := sql.Open("sqlite3", dbFileName)
	checkErr(err)
	rows, err := db.Query(fmt.Sprintf("SELECT obj_id FROM articles WHERE migration_status = '%s' LIMIT %d", status, limit))
	checkErr(err)
	var id string
	ids := make([]string, 0)
	for rows.Next() {
		err = rows.Scan(&id)
		checkErr(err)
		ids = append(ids, id)
	}
	rows.Close() //good habit to close
	err = db.Close()
	checkErr(err)
	if showTiming {
		fmt.Printf("Got %v ids in %v. \n", len(ids), time.Since(startTime))
	}
	return ids
}

// Делает последовательные запросы к API возвращая массив пар:
// [ [id, text], [id,text],...]
func getAPITexts(ids []string) [][]string {
	// startTime := time.Now()
	articles := make([][]string, 0)
	for _, id := range ids {
		articles = append(articles, getOneArticleFromAPI(id))
	}
	// duration := time.Since(startTime)
	// fmt.Printf("Got %v articles in %v. \n", len(ids), duration)
	return articles
}

// Делает параллельные запросы к API возвращая массив пар:
// [ [id, text], [id,text],...]
func getAPITextsParallel(ids []string, showTiming bool) [][]string {
	startTime := time.Now()
	articles := make([][]string, 0)
	ch := make(chan []string)

	for _, id := range ids {
		go func(id string) {
			ch <- getOneArticleFromAPI(id)
		}(id)
	}

	for range ids {
		v := <-ch
		articles = append(articles, v)
	}
	close(ch)
	if showTiming {
		fmt.Printf("Got %v articles in %v. \n", len(ids), time.Since(startTime))
	}
	return articles
}

// Возвращает id материала и его текст в виде [id, text] из API
func getOneArticleFromAPI(id string) []string {
	client := http.Client{
		Timeout: time.Duration(requestTimeout) * time.Second,
	}

	req, err := http.NewRequest("GET", fmt.Sprintf(urlArticle, id), nil)
	if err != nil {
		fmt.Println(err)
	}
	req.Close = true
	req.Header.Set("Connection", "close")

	resp, err := client.Do(req)

	// resp, err := http.Get(fmt.Sprintf(urlArticle, id))
	if err != nil {
		fmt.Println(err)
		return []string{id, ""}
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return []string{id, ""}
	}
	s := string(body)
	return []string{id, s}
}

// Преобразует массив текстов в массив записей.
// Запись это отображение: имя_поля -> значение_поля
func textsToArticleRecords(texts [][]string) []map[string]interface{} {
	records := make([]map[string]interface{}, 0)
	for _, o := range texts {
		id := o[0]
		text := o[1]
		// record := map[string]string{"obj_id": id}
		var objmap map[string]interface{} //json.RawMessage
		err := json.Unmarshal([]byte(text), &objmap)
		if err != nil {
			fmt.Println(err)
			objmap = make(map[string]interface{})
			objmap["obj_id"] = id
			objmap["migration_status"] = "error"
		} else {
			objmap["migration_status"] = "success"
		}
		records = append(records, objmap)
	}
	return records
}

// Сохраняет массив записей в базу данных.
// Запись представляет собой map[string]interface{}.
func saveArticlesToDatabase(records []map[string]interface{}, showTiming bool) {
	startTime := time.Now()

	paramsArray := make([][]interface{}, 0)

	for _, record := range records {
		params := make([]interface{}, 0)
		params = append(params, getMapVal(record, "announce"))
		params = append(params, getMapVal(record, "authors"))
		params = append(params, getMapVal(record, "date_modified"))
		params = append(params, getMapVal(record, "full-text"))
		params = append(params, getMapVal(record, "images"))
		params = append(params, getMapVal(record, "index_priority"))
		params = append(params, getMapVal(record, "is_active"))
		params = append(params, getMapVal(record, "is_announce"))
		params = append(params, getMapVal(record, "is_paid"))
		params = append(params, getMapVal(record, "link_title"))
		params = append(params, getMapVal(record, "links"))
		params = append(params, getMapVal(record, "obj_kind"))
		params = append(params, getMapVal(record, "projects"))
		params = append(params, getMapVal(record, "release_date"))
		params = append(params, getMapVal(record, "spiegel"))
		params = append(params, getMapVal(record, "title"))
		params = append(params, getMapVal(record, "uannounce"))
		params = append(params, getMapVal(record, "url"))
		params = append(params, getMapVal(record, "migration_status"))
		params = append(params, getMapVal(record, "obj_id"))
		paramsArray = append(paramsArray, params)
	}

	sqlUpdate := `
		UPDATE articles
		SET 
			announce=? ,
			authors=? ,
			date_modified=? , 
			"full-text"=? ,
			images=? ,
			index_priority=? ,
			is_active=? ,
			is_announce=? ,
			is_paid=? ,
			link_title=? ,
			links=? , 
			obj_kind=? ,
			projects=? ,
			release_date=? ,
			spiegel=? ,
			title=? ,
			uannounce=? ,
			url=? ,
			migration_status=? 
		WHERE 
			obj_id=?
	`
	execMany(sqlUpdate, paramsArray)
	if showTiming {
		fmt.Printf("Saved %v articles to database in %v. \n", len(records), time.Since(startTime))
	}
}

// Получает значение поля из отображения.
// Возвращает NULL в случае отсутствия поля,
// и тестовое представление если поле содержит JSON.
func getMapVal(m map[string]interface{}, key string) interface{} {
	v, ok := m[key]
	if !ok {
		return nil
	}
	s, ok := v.(string)
	if ok {
		return s
	}

	b, err := json.Marshal(v)
	if err == nil {
		s = string(b)
	}
	return s
}

// Исполняет запрос к базе данных
func exec(sqlText string) {
	db, err := sql.Open("sqlite3", dbFileName)
	defer db.Close()
	checkErr(err)
	stmt, err := db.Prepare(sqlText)
	defer stmt.Close()
	checkErr(err)
	_, err = stmt.Exec()
	checkErr(err)
}

// Исполняет несколько параметризованных запросов на обновление или вставку.
// Если запрос не прошел, печатает сообщение.
func execMany(sqlText string, paramsArray [][]interface{}) {
	db, err := sql.Open("sqlite3", dbFileName)
	// defer db.Close()
	checkErr(err)
	stmt, err := db.Prepare(sqlText)
	checkErr(err)

	for _, params := range paramsArray {
		res, err := stmt.Exec(params...)
		checkErr(err)
		// Если запрос не затронул ни одну запись, выводим сообщение.
		affect, err := res.RowsAffected()
		checkErr(err)
		if affect == 0 {
			fmt.Println("Affected->", affect)
		}
	}
	err = stmt.Close()
	checkErr(err)
	err = db.Close()
	checkErr(err)
}

// Печатаем сообщение об ошибке
func checkErr(err error) {
	if err != nil {
		fmt.Print(err)
	}
}