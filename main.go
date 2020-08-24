package main

import (
	"database/sql"
	"fmt"
	"io/ioutil"
	"net/http"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

var dbFileName = `rg.db`
var pageSize = 5
var pageCount = 0
var urlArticle = "https://outer.rg.ru/plain/proxy/?query=https://rg.ru/api/get/object/article-%v.json"

func main() {
	// Порождаем таблицу articles
	// createArticlesTable()
	// Заполняем ее пустыми записями с идентификаторами из таблицы rubrics_articles
	// fillArticlesWithIds()
	//Берем первую порцию идентификаторов из таблицы articles
	ids := getArticleIds(pageSize)
	// Если в порции есть идентификаторы
	for len(ids) > 0 {
		//Запрашиваем тексты статей
		articles := getArticlesFromAPI(ids)
		// Сохраняем их в базу данных
		saveArticles(articles)
		// Берем следующую порцию идентификаторов
		time.Sleep(time.Second)
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

func getArticlesFromAPI(ids []string) []string {
	articles := make([]string, 0)
	for _, id := range ids {
		text, err := getOneArticleFromAPI(id)
		if err != nil {
			fmt.Println(err)
			continue
		}
		fmt.Println(text)
		articles = append(articles, text)
	}
	return articles
}

func getOneArticleFromAPI(id string) (string, error) {
	resp, err := http.Get(fmt.Sprintf(urlArticle, id))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}
	return string(body), nil

}

func saveArticles(articles []string) {
	fmt.Printf("#%v Saved articles %v\n", pageCount, articles)
	pageCount++
}

func exec(sqlText string) {
	db, err := sql.Open("sqlite3", dbFileName)
	checkErr(err)
	stmt, err := db.Prepare(sqlText)
	checkErr(err)
	_, err = stmt.Exec()
	checkErr(err)
	err = db.Close()
	checkErr(err)
}

func checkErr(err error) {
	if err != nil {
		fmt.Print(err)
	}
}
