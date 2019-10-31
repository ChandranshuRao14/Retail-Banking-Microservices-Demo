package main

import (
	"context"
	"net/http"
	"encoding/json"
	//"os"
	//"io"
	"log"
	//"fmt"
	"strings"
	//"path"
	"github.com/gorilla/mux"
	//"github.com/gorilla/handlers"
	"strconv"
	"google.golang.org/appengine"
	//"google.golang.org/appengine/datastore"
	"cloud.google.com/go/datastore"
)

// Kind in Datastore
type User struct {
	UserID int64 `json: "userid"`
	Username string `json: "username"`
	AccountBalance float64 `json: "accountbalance"`
}

var dsClient *datastore.Client

func main() {
	ctx := context.Background()

	var err error
	// project ID
	dsClient, err = datastore.NewClient(ctx, "meganzhao-test")
	if err != nil {
		log.Fatal(err)
	}

	registerHandlers()
	appengine.Main()
}

func registerHandlers() {
	r := mux.NewRouter()
	r.HandleFunc("/", createHandler).Methods("POST")
	r.HandleFunc("/user/{id}", readHandler).Methods("GET")
	r.HandleFunc("/user/delete/{id}", deleteHandler).Methods("DELETE")
	r.HandleFunc("/user/update/{id}", updateHandler).Methods("PUT")
	log.Fatal(http.ListenAndServe(":8080", r))
}

// createHandler adds a user to the database.
func createHandler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)

	var user User
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	key := datastore.IncompleteKey("User", nil)
	if _, err := dsClient.Put(ctx, key, &user); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func readHandler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)
	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/"))
	if err != nil {
		// change error to invalid ID (should be an int)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	user := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	// have to use a slice to save the result? or have to use getall?
	if _, err := dsClient.GetAll(ctx, q, &user); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	res, _ := json.Marshal(&user)
	w.Write(res)
}

func deleteHandler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)
	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/delete/"))
	if err != nil {
		// todo: change error to invalid ID (should be an int)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	user := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	// have to use a slice to save the result? or have to use getall?
	keys, err := dsClient.GetAll(ctx, q, &user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	// todo: fix error message
	if err := dsClient.DeleteMulti(ctx, keys); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return		
	}
}

// createHandler adds a user to the database.
func updateHandler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)

	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/update/"))
	if err != nil {
		// todo: change error to invalid ID (should be an int)
		http.Error(w, err.Error(), http.StatusPaymentRequired)
		return
	}
	users := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	// have to use a slice to save the result? or have to use getall?
	keys, err := dsClient.GetAll(ctx, q, &users)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	var user User
	err = json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	if _, err := dsClient.Put(ctx, keys[0], &user); err != nil {
		http.Error(w, err.Error(), http.StatusPermanentRedirect)
		return
	}
}


// 	// Respond to App Engine and Compute Engine health checks.
// 	// Indicate the server is healthy.
// 	// r.Methods("GET").Path("/_ah/health").HandlerFunc(
// 	// 	func(w http.ResponseWriter, r *http.Request) {
// 	// 		w.Write([]byte("ok"))
// 	// 	})
		
// 	// Delegate all of the HTTP routing and serving to the gorilla/mux router.
// 	// Log all requests using the standard Apache format.
// 	// http.Handle("/", handlers.CombinedLoggingHandler(os.Stderr, r))
// }











