package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

var dbFileName = `rg.db`
var pageSize = 20
var pageCount = 0
var urlArticle = "https://outer.rg.ru/plain/proxy/?query=https://rg.ru/api/get/object/article-%v.json"
var sleepTime = time.Second

func main() {
	// Порождаем таблицу articles
	createArticlesTable()
	// Заполняем ее пустыми записями с идентификаторами из таблицы rubrics_articles
	//fillArticlesWithIds()
	//Берем первую порцию идентификаторов из таблицы articles
	ids := getArticleIds(pageSize)
	// Если в порции есть идентификаторы
	for len(ids) > 0 {
		//Запрашиваем тексты статей
		articleTexts := getArticlesFromAPI(ids)
		articleRecords := textsToRecords(articleTexts)
		// Сохраняем их в базу данных
		saveArticles(articleRecords)
		// Берем следующую порцию идентификаторов
		time.Sleep(sleepTime)
		ids = getArticleIds(pageSize)
	}

	// Когда нет больше идентификаторов, завершаем.
	fmt.Println("DONE")
}

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

func getArticleIds(limit int) []string {
	db, err := sql.Open("sqlite3", dbFileName)
	checkErr(err)
	rows, err := db.Query("SELECT obj_id FROM articles WHERE migration_status = '' LIMIT " + fmt.Sprint(limit))
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
	return ids
}

func getArticlesFromAPI(ids []string) [][]string {
	startTime := time.Now()
	articles := make([][]string, 0)
	for _, id := range ids {
		text := getOneArticleFromAPI(id)
		articles = append(articles, []string{id, text})
	}
	duration := time.Since(startTime)
	fmt.Printf("Got %v articles in %v. \n", len(ids), duration)
	return articles
}

func getOneArticleFromAPI(id string) string {
	resp, err := http.Get(fmt.Sprintf(urlArticle, id))
	if err != nil {
		fmt.Println(err)
		return ""
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	s := string(body)
	return s

}

func textsToRecords(texts [][]string) []map[string]string {
	records := make([]map[string]string, 0)
	for _, o := range texts {
		id := o[0]
		text := o[1]
		record := map[string]string{"obj_id": id}
		var objmap map[string]json.RawMessage
		err := json.Unmarshal([]byte(text), &objmap)
		if err != nil {
			fmt.Println(err)
			record["migration_status"] = "error"
		} else {
			record["migration_status"] = "success"
			for key, val := range objmap {
				record[key] = string(val)
			}
		}
		records = append(records, record)
	}
	return records
}

func saveArticles(records []map[string]string) {
	fmt.Printf("#%v Saving articles \n", pageCount)
	pageCount++

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
}

func getMapVal(m map[string]string, key string) interface{} {
	v, ok := m[key]
	if !ok {
		return nil
	}
	v = strings.Trim(v, "\"")
	return v
}

func exec(sqlText string) {
	db, err := sql.Open("sqlite3", dbFileName)
	defer db.Close()
	checkErr(err)
	stmt, err := db.Prepare(sqlText)
	defer stmt.Close()
	checkErr(err)
	_, err = stmt.Exec()
	checkErr(err)
	// err = db.Close()
	// checkErr(err)
}

func execMany(sqlText string, paramsArray [][]interface{}) {
	db, err := sql.Open("sqlite3", dbFileName)
	// defer db.Close()
	checkErr(err)
	stmt, err := db.Prepare(sqlText)
	checkErr(err)

	for _, params := range paramsArray {
		res, err := stmt.Exec(params...)
		checkErr(err)
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

func checkErr(err error) {
	if err != nil {
		fmt.Print(err)
	}
}
