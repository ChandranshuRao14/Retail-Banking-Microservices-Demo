package main

import (
	"context"
	"encoding/json"
	"net/http"
	"os"
	"fmt"
	"log"
	"strings"
	"github.com/gorilla/mux"
	"strconv"

	"golang.org/x/oauth2/google"
	"google.golang.org/api/option"

	"cloud.google.com/go/datastore"
)

// Kind in Datastore
type User struct {
	UserID         int64   `json: "userid"`
	Username       string  `json: "username"`
	Address        string  `json: "address"`
	Email          string  `json: "email"`
	Password       string  `json: "password"`
	PhoneNumber    int64   `json: "phonenumber"`
	AccountBalance float64 `json: "accountbalance"`
}

var dsClient *datastore.Client

func main() {
	ctx := context.Background()
	var err error
	creds, err := google.CredentialsFromJSON(ctx, []byte(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")), datastore.ScopeDatastore)
	if err != nil {
		// fmt.Printf("Can't retrieve service account key: %v\n", err)
		// return
	}
	dsClient, err = datastore.NewClient(ctx, os.Getenv("PROJECT_ID"), option.WithCredentials(creds))
	if err != nil {
		fmt.Printf("Can't retrieve project ID: %v\n", err)
		return

	}
	registerHandlers()
}

func registerHandlers() {
	r := mux.NewRouter()
	r.HandleFunc("/user", createHandler).Methods("POST")
	r.HandleFunc("/user", listHandler).Methods("GET")
	r.HandleFunc("/user/{id}", readHandler).Methods("GET")
	r.HandleFunc("/user/{id}", deleteHandler).Methods("DELETE")
	r.HandleFunc("/user/{id}", updateHandler).Methods("PUT")
	log.Fatal(http.ListenAndServe(":8080", r))
}

// CreateHandler adds a user to the database.
func createHandler(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	var user User
	// Decode request body
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	// Insert the entity into Datastore
	key := datastore.IncompleteKey("User", nil)
	key, err = dsClient.Put(ctx, key, &user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	user.UserID = key.ID
	// Update the entity with UUID
	if _, err = dsClient.Put(ctx, key, &user); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}	
	w.Write([]byte(fmt.Sprintf("%+v\n", user)))
}

func listHandler(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	user := make([]*User, 0)
	q := datastore.NewQuery("User")
	if _, err := dsClient.GetAll(ctx, q, &user); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	res, _ := json.Marshal(&user)
	w.Write(res)
}

func readHandler(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	users := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	if _, err := dsClient.GetAll(ctx, q, &users); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if len(users) == 0 {
		http.Error(w, "{'error': 'User ID not found'}", http.StatusBadRequest)
		return		
	}
	res, _ := json.Marshal(&users[0])
	w.Write(res)
}

func deleteHandler(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	user := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	keys, err := dsClient.GetAll(ctx, q, &user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if len(user) == 0 {
		http.Error(w, "{'error': 'User ID not found'}", http.StatusBadRequest)
		return		
	}
	if err := dsClient.DeleteMulti(ctx, keys); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write([]byte("Successfully deleted user " + fmt.Sprintf("%+v\n", user[0])))
}

// createHandler adds a user to the database.
func updateHandler(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	id, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/user/"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	users := make([]*User, 0)
	q := datastore.NewQuery("User").Filter("UserID =", id)
	keys, err := dsClient.GetAll(ctx, q, &users)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	if len(users) == 0 {
		http.Error(w, "{'error': 'User ID not found'}", http.StatusBadRequest)
		return		
	}
	var user User
	err = json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	user.UserID = keys[0].ID
	if _, err := dsClient.Put(ctx, keys[0], &user); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write([]byte(fmt.Sprintf("%+v\n", user)))
}
