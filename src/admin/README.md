# README


## Getting started

Before running the application you will need a working PostgreSQL installation and a valid DSN (data source name) for connecting to the database.

Please open the `cmd/web/main.go` file and edit it to include your valid DSN as the default value.

```
cfg.db.dsn = env.GetString("DB_DSN", "YOUR DEFAULT DSN GOES HERE")
```

Note that this DSN must be in the format `user:pass@localhost:port/db` and **not** be prefixed with `postgres://`.

Make sure that you're in the root of the project directory, fetch the dependencies with `go mod tidy`, then run the application using `go run ./cmd/web`:

```
$ go mod tidy
$ go run ./cmd/web
```

Then visit [http://localhost:4444](http://localhost:4444) in your browser.

You can also start the application with live reload support by using the `run` task in the `Makefile`:

```
$ make run
```

## Project structure

Everything in the codebase is designed to be editable. Feel free to change and adapt it to meet your needs.

|     |     |
| --- | --- |
| **`assets`** | Contains the non-code assets for the application. |
| `↳ assets/emails/` | Contains email templates. |
| `↳ assets/migrations/` | Contains SQL migrations. |
| `↳ assets/static/` | Contains static UI files (images, CSS etc). |
| `↳ assets/templates/` | Contains HTML templates. |
| `↳ assets/efs.go` | Declares an embedded filesystem containing all the assets. |

|     |     |
| --- | --- |
| **`cmd/web`** | Your application-specific code (handlers, routing, middleware, helpers) for dealing with HTTP requests and responses. |
| `↳ cmd/web/errors.go` | Contains helpers for managing and responding to error conditions. |
| `↳ cmd/web/handlers.go` | Contains your application HTTP handlers. |
| `↳ cmd/web/main.go` | The entry point for the application. Responsible for parsing configuration settings initializing dependencies and running the server. Start here when you're looking through the code. |
| `↳ cmd/web/middleware.go` | Contains your application middleware. |
| `↳ cmd/web/routes.go` | Contains your application route mappings. |
| `↳ cmd/web/templates.go` | Contains helpers for working with HTML templates. |
| `↳ cmd/web/server.go` | Contains a helper functions for starting and gracefully shutting down the server. |

|     |     |
| --- | --- |
| **`internal`** | Contains various helper packages used by the application. |
| `↳ internal/cookies` | Contains helper functions for reading/writing signed and encrypted cookies. |
| `↳ internal/database/` | Contains your database-related code (setup, connection and queries). |
| `↳ internal/env` | Contains helper functions for reading configuration settings from environment variables. |
| `↳ internal/funcs/` | Contains custom template functions. |
| `↳ internal/leveledlog/` | Contains a leveled logger implementation. |
| `↳ internal/request/` | Contains helper functions for decoding HTML forms, JSON requests, and URL query strings. |
| `↳ internal/response/` | Contains helper functions for rendering HTML templates and sending JSON responses. |
| `↳ internal/smtp/` | Contains a SMTP sender implementation. |
| `↳ internal/validator/` | Contains validation helpers. |
| `↳ internal/version/` | Contains the application version number definition. |

## Configuration settings

Configuration settings are managed via environment variables, with the environment variables read into your application in the `run()` function in the `main.go` file.

You can try this out by setting a `HTTP_PORT` environment variable to configure the network port that the server is listening on:

```
$ export HTTP_PORT="9999"
$ go run ./cmd/web
level="INFO" time="2023-01-28T09:14:11Z" message="starting server on :9999"
```

Feel free to adapt the `run()` function to parse additional environment variables and store their values in the `config` struct. The application uses helper functions in the `internal/env` package to parse environment variable values or return a default value if no matching environment variable is set. It includes `env.GetString()`, `env.GetInt()` and `env.GetBool()` functions for reading string, integer and bool values from environment variables. Again, you can add any additional helper functions that you need.

## Creating new handlers

Handlers are defined as `http.HandlerFunc` methods on the `application` struct. They take the pattern:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    // Your handler logic...
}
```

Handlers are defined in the `cmd/web/handlers.go` file. For small applications, it's fine for all handlers to live in this file. For larger applications (10+ handlers) you may wish to break them out into separate files.

## Handler dependencies

Any dependencies that your handlers have should be initialized in the `run()` function `cmd/web/main.go` and added to the `application` struct. All of your handlers, helpers and middleware that are defined as methods on `application` will then have access to them.

You can see an example of this in the `cmd/web/main.go` file where we initialize a new `logger` instance and add it to the `application` struct.

## Creating new routes

[Flow](https://github.com/alexedwards/flow) is used for routing. Routes are defined in the `routes()` method in the `cmd/web/routes.go` file. For example:

```
func (app *application) routes() http.Handler {
    mux := flow.New()

    mux.HandleFunc("/your/path", app.yourHandler, "GET")

    return mux
}
```

For more information about Flow and example usage, please see the [official documentation](https://github.com/alexedwards/flow).

## Adding middleware

Middleware is defined as methods on the `application` struct in the `cmd/web/middleware.go` file. Feel free to add your own. They take the pattern:

```
func (app *application) yourMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Your middleware logic...
        next.ServeHTTP(w, r)
    })
}
```

You can then register this middleware with the router using the `Use()` method:

```
func (app *application) routes() http.Handler {
    mux := flow.New()
    mux.Use(app.yourMiddleware)

    mux.HandleFunc("/your/path", app.yourHandler, "GET")

    return mux
}
```

It's possible to use middleware on specific routes only by creating route 'groups':

```
func (app *application) routes() http.Handler {
    mux := flow.New()
    mux.Use(app.yourMiddleware)

    mux.HandleFunc("/your/path", app.yourHandler, "GET")

    mux.Group(func(mux *flow.Mux) {
        mux.Use(app.yourOtherMiddleware)

        mux.HandleFunc("/your/other/path", app.yourOtherHandler, "GET")
    })

    return mux
}
```

Note: Route 'groups' can also be nested.

## Rendering HTML templates

HTML templates are stored in the `assets/templates` directory and use the standard library `html/template` package. The structure looks like this:

|     |     |
| --- | --- |
| `assets/templates/base.tmpl` | The 'base' template containing the shared HTML markup for all your web pages. |
| `assets/templates/pages/` | Directory containing files with the page-specific content for your web pages. See `assets/templates/pages/home.tmpl` for an example. |
| `assets/templates/partials/` | Directory containing files with 'partials' to embed in your web pages or base template. See `assets/templates/partials/footer.tmpl` for an example. |

The HTML for web pages can be sent using the `response.Page()` function. For convenience, an `app.newTemplateData()` method is provided which returns a `map[string]any` map. You can add data to this map and pass it on to your templates.

For example, to render the HTML in a `assets/templates/pages/example.tmpl` file:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    data := app.newTemplateData()
    data["hello"] = "world"

    err := response.Page(w, http.StatusOK, data, "pages/example.tmpl")
    if err != nil {
        app.serverError(w, r, err)
    }
}
```

Specific HTTP headers can optionally be sent with the response too:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    data := app.newTemplateData()
    data["hello"] = "world"

    headers := make(http.Header)
    headers.Set("X-Server", "Go")

    err := response.PageWithHeaders(w, http.StatusOK, data, headers, "pages/example.tmpl")
    if err != nil {
        app.serverError(w, r, err)
    }
}
```

Note: All the files in the `assets/templates` directory are embedded into your application binary and can be accessed via the `EmbeddedFiles` variable in `assets/efs.go`.

## Adding default template data

If you have data that you want to display or use on multiple web pages, you can adapt the `newTemplateData()` helper in the `templates.go` file to include this by default. For example, if you wanted to include the current year value you could adapt it like this:

```
func (app *application) newTemplateData() map[string]any {
    data := map[string]any{
        "CurrentYear": time.Now().Year(),
    }

    return data
}
```

## Custom template functions

Custom template functions are defined in `internal/funcs/funcs.go` and are automatically made available to your

HTML templates when you use `response.Page()` and email templates when you use `app.mailer.Send()`
.

The following custom template functions are already included by default:

|     |     |
| --- | --- |
| `now` | Returns the current time. |
| `timeSince arg1` | Returns the time elapsed since arg1. |
| `timeUntil arg2` | Returns the time until arg1. |
| `formatTime arg1 arg2` | Returns the time arg2 as formatted using the pattern arg1. |
| `approxDuration arg1` | Returns the approximate duration of arg1 in a 'human-friendly' format ("3 seconds", "2 months", "5 years") etc. |
| `uppercase arg1` | Returns arg1 converted to uppercase. |
| `lowercase arg1` | Returns arg1 converted to lowercase. |
| `pluralize arg1 arg2 arg3` | If arg1 equals 1 then return arg2, otherwise return arg3. |
| `slugify arg1` | Returns the lowercase of arg1 with all non-ASCII characters and punctuation removed (expect underscores and hyphens). Whitespaces are also replaced with a hyphen. |
| `safeHTML arg1` | Output the verbatim value of arg1 without escaping the content. This should only be used when arg1 is from a trusted source. |
| `join arg1 arg2` | Returns the values in arg1 joined using the separator arg2. |
| `containsString arg1 arg2 ` | Returns true if arg1 contains the string value arg2. |
| `incr arg1` | Increments arg1 by 1. |
| `decr arg1` | Decrements arg1 by 1. |
| `formatInt arg1` | Returns arg1 formatted with commas as the thousands separator. |
| `formatFloat arg1 arg2` | Returns arg1 rounded to arg2 decimal places and formatted with commas as the thousands separator. |
| `yesno arg1` | Returns "Yes" if arg1 is true, or "No" if arg1 is false. |
| `urlSetParam arg1 arg2 arg3` | Returns the URL arg1 with the key arg2 and value arg3 added to the query string parameters. |
| `urlDelParam arg1 arg2` | Returns the URL arg1 with the key arg2 (and corresponding value) removed from the query string parameters. |

To add another custom template function, define the function in `internal/funcs/funcs.go` and add it to the `TemplateFuncs` map. For example:

```
var TemplateFuncs = template.FuncMap{
    ...
    "yourFunction": yourFunction,
}

func yourFunction(s string) (string, error) {
    // Do something...
}
```

## Static files

By default, the files in the `assets/static` directory are served using Go's `http.Fileserver` whenever the application receives a `GET` request with a path beginning `/static/`. So, for example, if the application receives a `GET /static/css/main.css` request it will respond with the contents of the `assets/static/css/main.css` file.

If you want to change or remove this behavior you can by editing the `routes.go` file.

Note: The files in `assets/static` directory are embedded into your application binary and can be accessed via the `EmbeddedFiles` variable in `assets/efs.go`.

## Working with forms

The codebase includes a `request.DecodePostForm()` function for automatically decoding HTML form data into a struct, and `request.DecodeQueryString()` for decoding URL query strings into a struct. Behind the scenes this decoding is managed using the [go-playground/form](https://github.com/go-playground/form) package.

As an example, let's say you have a page with the following HTML form for creating a 'person' record and routing rule:

```
<form action="/person/create" method="POST">
    <div>
        <label>Your name:</label>
        <input type="text" name="Name" value="{{.Form.Name}}">
    </div>
    <div>
        <label>Your age:</label>
        <input type="number" name="Age" value="{{.Form.Age}}">
    </div>
    <button>Submit</button>
</form>
```

```
func (app *application) routes() http.Handler {
    mux := flow.New()

    mux.HandleFunc("/person/create", app.createPerson, "GET", "POST")

    return mux
}
```

Then you can display and parse this form with a `createPerson` handler like this:

```
package main

import (
    "net/http"

    "pks.pyfreebilling.com/internal/request"
    "pks.pyfreebilling.com/internal/response"
)

func (app *application) createPerson(w http.ResponseWriter, r *http.Request) {
    type createPersonForm struct {
        Name string `form:"Name"`
        Age  int    `form:"Age"`
    }

    switch r.Method {
    case http.MethodGet:
        data := app.newTemplateData()

        // Add any default values to the form.
        data["Form"] = createPersonForm{
            Age: 21,
        }

        err := response.Page(w, http.StatusOK, data, "/path/to/page.tmpl")
        if err != nil {
            app.serverError(w, r, err)
        }

    case http.MethodPost:
        var form createPersonForm

        err := request.DecodePostForm(r, &form)
        if err != nil {
            app.badRequest(w, r, err)
            return
        }

        // Do something with the data in the form variable...
    }
}
```

## Validating forms

The `internal/validator` package includes a simple (but powerful) `validator.Validator` type that you can use to carry out validation checks.

Extending the example above:

```
package main

import (
    "net/http"

    "pks.pyfreebilling.com/internal/request"
    "pks.pyfreebilling.com/internal/response"
    "pks.pyfreebilling.com/internal/validator"
)

func (app *application) createPerson(w http.ResponseWriter, r *http.Request) {
    type createPersonForm struct {
        Name      string              `form:"Name"`
        Age       int                 `form:"Age"`
        Validator validator.Validator `form:"-"`
    }

    switch r.Method {
    case http.MethodGet:
        data := app.newTemplateData()

        // Add any default values to the form.
        data["Form"] = createPersonForm{
            Age: 21,
        }

        err := response.Page(w, http.StatusOK, data, "/path/to/page.tmpl")
        if err != nil {
            app.serverError(w, r, err)
        }

    case http.MethodPost:
        var form createPersonForm

        err := request.DecodePostForm(r, &form)
        if err != nil {
            app.badRequest(w, r, err)
            return
        }

        form.Validator.CheckField(form.Name != "", "Name", "Name is required")
        form.Validator.CheckField(form.Age != 0, "Age", "Age is required")
        form.Validator.CheckField(form.Age >= 21, "Age", "Age must be 21 or over")

        if form.Validator.HasErrors() {
            data := app.newTemplateData()
            data["Form"] = form

            err := response.Page(w, http.StatusUnprocessableEntity, data, "/path/to/page.tmpl")
            if err != nil {
                app.serverError(w, r, err)
            }
            return
        }

        // Do something with the form information, like adding it to a database...
    }
}
```

And you can display the error messages in your HTML form like this:

```
<form action="/person/create" method="POST">
    {{if .Form.Validator.HasErrors}}
        <p>Something was wrong. Please correct the errors below and try again.</p>
    {{end}}
    <div>
        <label>Your name:</label>
        {{with .Form.Validator.FieldErrors.Name}}
            <span class='error'>{{.}}</span>
        {{end}}
        <input type="text" name="Name" value="{{.Form.Name}}">
    </div>
    <div>
        <label>Your age:</label>
        {{with .Form.Validator.FieldErrors.Age}}
            <span class='error'>{{.}}</span>
        {{end}}
        <input type="number" name="Age" value="{{.Form.Age}}">
    </div>
    <button>Submit</button>
</form>
```

In the example above we use the `CheckField()` method to carry out validation checks for specific fields. You can also use the `Check()` method to carry out a validation check that is _not related to a specific field_. For example:

```
input.Validator.Check(input.Password == input.ConfirmPassword, "Passwords do not match")
```

The `validator.AddError()` and `validator.AddFieldError()` methods also let you add validation errors directly:

```
input.Validator.AddFieldError("Email", "This email address is already taken")
input.Validator.AddError("Passwords do not match")
```

The `internal/validator/helpers.go` file also contains some helper functions to simplify validations that are not simple comparison operations.

|     |     |
| --- | --- |
| `NotBlank(value string)` | Check that the value contains at least one non-whitespace character. |
| `MinRunes(value string, n int)` | Check that the value contains at least n runes. |
| `MaxRunes(value string, n int)` | Check that the value contains no more than n runes. |
| `Between(value, min, max T)` | Check that the value is between the min and max values inclusive. |
| `Matches(value string, rx *regexp.Regexp)` | Check that the value matches a specific regular expression. |
| `In(value T, safelist ...T)` | Check that a value is in a 'safelist' of specific values. |
| `AllIn(values []T, safelist ...T)` | Check that all values in a slice are in a 'safelist' of specific values. |
| `NotIn(value T, blocklist ...T)` | Check that the value is not in a 'blocklist' of specific values. |
| `NoDuplicates(values []T)` | Check that a slice does not contain any duplicate (repeated) values. |
| `IsEmail(value string)` | Check that the value has the formatting of a valid email address. |
| `IsURL(value string)` | Check that the value has the formatting of a valid URL. |

For example, to use the `Between` check your code would look similar to this:

```
input.Validator.CheckField(validator.Between(input.Age, 18, 30), "Age", "Age must between 18 and 30")
```

Feel free to add your own helper functions to the `internal/validator/helpers.go` file as necessary for your application.

## Sending JSON responses

JSON responses and a specific HTTP status code can be sent using the `response.JSON()` function. The `data` parameter can be any JSON-marshalable type.

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    data := map[string]string{"hello":  "world"}

    err := response.JSON(w, http.StatusOK, data)
    if err != nil {
        app.serverError(w, r, err)
    }
}
```

Specific HTTP headers can optionally be sent with the response too:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    data := map[string]string{"hello":  "world"}

    headers := make(http.Header)
    headers.Set("X-Server", "Go")

    err := response.JSONWithHeaders(w, http.StatusOK, data, headers)
    if err != nil {
        app.serverError(w, r, err)
    }
}
```

## Parsing JSON requests

HTTP requests containing a JSON body can be decoded using the `request.DecodeJSON()` function. For example, to decode JSON into an `input` struct:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Name string `json:"Name"`
        Age  int    `json:"Age"`
    }

    err := request.DecodeJSON(w, r, &input)
    if err != nil {
        app.badRequest(w, r, err)
        return
    }

    ...
}
```

Note: The target decode destination passed to `request.DecodeJSON()` (which in the example above is `&input`) must be a non-nil pointer.

The `request.DecodeJSON()` function returns friendly, well-formed, error messages that are suitable to be sent directly to the client using the `app.badRequest()` helper.

There is also a `request.DecodeJSONStrict()` function, which works in the same way as `request.DecodeJSON()` except it will return an error if the request contains any JSON fields that do not match a name in the the target decode destination.

## Validating JSON requests

The `internal/validator` package includes a simple (but powerful) `validator.Validator` type that you can use to carry out validation checks.

Extending the example above:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Name      string              `json:"Name"`
        Age       int                 `json:"Age"`
        Validator validator.Validator `json:"-"`
    }

    err := request.DecodeJSON(w, r, &input)
    if err != nil {
        app.badRequest(w, r, err)
        return
    }

    input.Validator.CheckField(input.Name != "", "Name", "Name is required")
    input.Validator.CheckField(input.Age != 0, "Age", "Age is required")
    input.Validator.CheckField(input.Age >= 21, "Age", "Age must be 21 or over")

    if input.Validator.HasErrors() {
        app.failedValidation(w, r, input.Validator)
        return
    }

    ...
}
```

The `app.failedValidation()` helper will send a `422` status code along with any validation error messages. For the example above, the JSON response will look like this:

```
{
    "FieldErrors": {
        "Age": "Age must be 21 or over",
        "Name": "Name is required"
    }
}
```

## Working with the database

This codebase is set up to use PostgreSQL with the [lib/pq](https://github.com/lib/pq) driver. You can control which database you connect to using the `DB_DSN` environment variable to pass in a DSN, or by adapting the default value in `run()`.

The codebase is also configured to use [jmoiron/sqlx](https://github.com/jmoiron/sqlx), so you have access to the whole range of sqlx extensions as well as the standard library `Exec()`, `Query()` and `QueryRow()` methods .

The database is available to your handlers, middleware and helpers via the `application` struct. If you want, you can access the database and carry out queries directly. For example:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    ...

    _, err := app.db.Exec("INSERT INTO people (name, age) VALUES ($1, $2)", "Alice", 28)
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    ...
}
```

Generally though, it's recommended to isolate your database logic in the `internal/database` package and extend the `DB` type to include your own methods. For example, you could create a `internal/database/people.go` file containing code like:

```
type Person struct {
    ID    int    `db:"id"`
    Name  string `db:"name"`
    Age   int    `db:"age"`
}

func (db *DB) NewPerson(name string, age int) error {
    _, err := db.Exec("INSERT INTO people (name, age) VALUES ($1, $2)", name, age)
    return err
}

func (db *DB) GetPerson(id int) (Person, error) {
    var person Person
    err := db.Get(&person, "SELECT * FROM people WHERE id = $1", id)
    return person, err
}
```

And then call this from your handlers:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    ...

    _, err := app.db.NewPerson("Alice", 28)
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    ...
}
```

## Managing SQL migrations

The `Makefile` in the project root contains commands to easily create and work with database migrations:

|     |     |
| --- | --- |
| `$ make migrations/new name=add_example_table` | Create a new database migration in the `assets/migrations` folder. |
| `$ make migrations/up` | Apply all up migrations. |
| `$ make migrations/down` | Apply all down migrations. |
| `$ make migrations/goto version=N` | Migrate up or down to a specific migration (where N is the migration version number). |
| `$ make migrations/force version=N` | Force the database to be specific version without running any migrations. |
| `$ make migrations/version` | Display the currently in-use migration version. |

Hint: You can run `$ make help` at any time for a reminder of these commands.

These `Makefile` tasks are simply wrappers around calls to the `github.com/golang-migrate/migrate/v4/cmd/migrate` tool. For more information, please see the [official documentation](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate).

By default all 'up' migrations are automatically run on application startup using embeded files from the `assets/migrations` directory. You can disable this by setting the `DB_AUTOMIGRATE` environment variable to `false`.

## Logging

The `internal/leveledlog` package provides a leveled-logger implementation. It outputs color-coded log lines in the following format:

```
level="INFO" time="2022-08-15T08:51:09+02:00" message="starting server on localhost:4444 (version 0.0.1)"
```

By default, a logger is initialized in the `main()` function which writes all log messages to `os.Stdout`. You can call the logger's `Info()`, `Warn()`, `Error()` and `Fatal()` methods to log messages at different levels with `fmt.Printf` style formatting. For example:

```
logger.Info("starting server on %d", 1234)
```

Note: Calling `Fatal()` will cause your application to terminate.

Also note: Any messages that are automatically logged by the Go `http.Server` are output at `Warning()` level.

If you want to disable the color-coding, then pass `false` as the final parameter when initializing the logger in `main()`.

```
logger := leveledlog.NewLogger(os.Stdout, leveledlog.LevelAll, false)
```

You can also write JSON-formated log entries instead by using the `NewJSONLogger()` function to initialize the logger:

```
logger := leveledlog.NewJSONLogger(os.Stdout, leveledlog.LevelAll)
```

JSON-formatted log entries are not color-coded.

Feel free to adapt the `internal/leveledlog` package to change this behavior or include additional fields if you want.

## Cookies

The `internal/cookies` package provides helper functions for reading and writing cookies.

The `Write()` function base64-encodes the cookie value and checks the cookie length is no more than 4096 bytes before writing the cookie. You can use it like this:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    // Initialize a Go cookie as normal.
    cookie := http.Cookie{
        Name:     "exampleCookie",
        Value:    "Hello Zoë!",
        Path:     "/",
        MaxAge:   3600,
        HttpOnly: true,
        Secure:   true,
        SameSite: http.SameSiteLaxMode,
    }

    // Write the cookie.
    err := cookies.Write(w, cookie)
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    ...
}
```

The `Read()` function reads a named cookie and base64-decodes the value before returning it.

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    // Read the cookie value and handle any errors as necessary for your application.
    value, err := cookies.Read(r, "exampleCookie")
    if err != nil {
        switch {
        case errors.Is(err, http.ErrNoCookie):
            app.badRequest(w, r, err)
        case errors.Is(err, cookies.ErrInvalidValue):
            app.badRequest(w, r, err)
        default:
            app.serverError(w, r, err)
        }
        return
    }

    ...
}
```

The `internal/cookies` package also provides `WriteSigned()` and `ReadSigned()` functions for writing/reading signed cookies, and `WriteEncrypted()` and `ReadEncrypted()` functions encrypted cookies. Signed cookies are authenticated using HMAC-256, meaning that you can trust that the contents of the cookie has not been tampered with. Encrypted cookies are encrpyted using AES-GCM, which both authenticates and encrypts the cookie data, meaning that you can trust that the contents of the cookie has not been tampered with _and_ the contents of the cookie cannot be read by the client.

When using these helper functions, you must set your own (secret) key for signing and encryption. This key should be a random 32-character string generated using a CSRNG which you pass to the application using the `COOKIE_SECRET_KEY` environment variable. For example:

```
$ export COOKIE_SECRET_KEY="heoCDWSgJ430OvzyoLNE9mVV9UJFpOWx"
$ go run ./cmd/web
```

To write a new signed or encrypted cookie:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    // Initialize a Go cookie as normal.
    cookie := http.Cookie{
        Name:     "exampleCookie",
        Value:    "Hello Zoë!",
        Path:     "/",
        MaxAge:   3600,
        HttpOnly: true,
        Secure:   true,
        SameSite: http.SameSiteLaxMode,
    }

    // Write a signed cookie using WriteSigned() and passing in the secret key
    // as the final argument. Use WriteEncrypted() if you want an encrpyted
    // cookie instead.
    err := cookies.WriteSigned(w, cookie, app.config.cookie.secretKey)
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    ...
}
```

To read a signed or encrypted cookie:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    // Read the cookie value using ReadSigned() and passing in the secret key
    // as the final argument. Use ReadEncrypted() if you want to read an
    // encrpyted cookie instead.
    value, err := cookies.ReadSigned(r, "exampleCookie", app.config.cookie.secretKey)
    if err != nil {
        switch {
        case errors.Is(err, http.ErrNoCookie):
            app.badRequest(w, r, err)
        case errors.Is(err, cookies.ErrInvalidValue):
            app.badRequest(w, r, err)
        default:
            app.serverError(w, r, err)
        }
        return
    }

    ...
}
```

## Using Basic Authentication

The `cmd/web/middleware.go` file contains a `basicAuth` middleware that you can use to protect your application — or specific application routes — with HTTP basic authentication.

You can try this out by visiting the [https://localhost:4444//basic-auth-protected](https://localhost:4444//basic-auth-protected) endpoint in any web browser and entering the default user name and password:

```
User name: admin
Password:  pa55word
```

You can change the user name and password by setting the `BASIC_AUTH_USERNAME` environment variable and `BASIC_AUTH_HASHED_PASSWORD` environment variable. For example:

```
$ export BASIC_AUTH_USERNAME='alice'
$ export BASIC_AUTH_HASHED_PASSWORD='$2a$10$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
$ go run ./cmd/web
```

Note: You will probably need to wrap the username and password in `'` quotes to prevent your shell interpreting dollar and slash symbols as special characters.

The value for the `BASIC_AUTH_HASHED_PASSWORD` environment variable should be a bcrypt hash of the password, not the plaintext password itself. An easy way to generate the bcrypt hash for a password is to use the `gophers.dev/cmds/bcrypt-tool` package like so:

```
$ go run gophers.dev/cmds/bcrypt-tool@latest hash 'your_pa55word'
```

If you want to change the default values for username and password you can do so by editing the default command-line flag values in the `cmd/web/main.go` file.

## Using sessions

The codebase is set up so that cookie-based sessions (using the [gorilla/sessions](https://github.com/gorilla/sessions) package) work out-of-the-box.

You can use them in your handlers like this:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    ...

    session, err := app.sessionStore.Get(r, "sessions")
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    session.Values["foo"] = "bar"

    err = session.Save(r, w)
    if err != nil {
        app.serverError(w, r, err)
        return
    }

    ...
}
```

By default sessions are set to expire after 1 week. You can configure this along with other session cookie settings in the `cmd/web/main.go` file by changing the `sessions.Options` struct values:

```
sessionStore.Options = &sessions.Options{
    HttpOnly: true,
    MaxAge:   86400 * 7, // 1 week in seconds
    Path:     "/",
    SameSite: http.SameSiteLaxMode,
}
```

When running the application in production you should use your own secret key for authenticating sessions. This key should be a random 32-character string generated using a CSRNG which you pass to the application using the `SESSION_SECRET_KEY` environment variable.

```
$ export SESSION_SECRET_KEY="npsqT5At8USavGtyRpr4tc8j9hWK2Yol"
$ go run ./cmd/web
```

Key rotation is supported. If you want to switch to a new key run the application using the `SESSION_SECRET_KEY` environment variable for the new key and the `SESSION_OLD_SECRET_KEY` environment variablefor the old key, until all sessions using the old key have expired.

```
$ export SESSION_SECRET_KEY="SfvzdTUOHeHkavOzRP6p1uUVpueX11mW"
$ export SESSION_OLD_SECRET_KEY="npsqT5At8USavGtyRpr4tc8j9hWK2Yol"
$ go run ./cmd/web
```

For more information please see the [documentation for the gorilla/sessions package](https://github.com/gorilla/sessions).

## Sending emails

The application is configured to support sending of emails via SMTP.

Email templates should be defined as files in the `assets/emails` folder. Each file should contain named templates for the email subject, plaintext body and — optionally — HTML body.

```
{{define "subject"}}Example subject{{end}}

{{define "plainBody"}}
This is an example body
{{end}}

{{define "htmlBody"}}
<!doctype html>
<html>
    <head>
        <meta name="viewport" content="width=device-width" />
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
        <p>This is an example body</p>
    </body>
</html>
{{end}}
```

A further example can be found in the `assets/emails/example.tmpl` file. Note that your email templates automatically have access to the custom template functions defined in the `internal/funcs` package.

Emails can be sent from your handlers using `app.mailer.Send()`. For example, to send an email to `alice@example.com` containing the contents of the `assets/emails/example.tmpl` file:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    ...

    data := map[string]any{"Name": "Alice"}

    err := app.mailer.Send("alice@example.com", data, "example.tmpl")
    if err != nil {
        app.serverError(w, r, err)
        return
    }

   ...
}
```

Note: The second parameter to `Send()` should be a map or struct containing any dynamic data that you want to render in the email template.

The SMTP host, port, username, password and sender details can be configured using the `SMTP_HOST` environment variable, `SMTP_PORT` environment variable, `SMTP_USERNAME` environment variable, `SMTP_PASSWORD` environment variable, and `SMTP_FROM` environment variable or by adapting the default values in `cmd/web/main.go`.

You may wish to use [Mailtrap](https://mailtrap.io/) or a similar tool for development purposes.

## Error notifications

The application supports sending alerts for runtime errors to an admin email address. You can enable this by setting the `NOTIFICATIONS_EMAIL` environment variable to a valid email address.

If you don't set a value for this, then no notifications will be sent (but the errors will still be logged).

Notifications will only be sent for any errors that are encountered as part of a request-response cycle (i.e. whenever a user sees an '500 Internal Server Error' response). Notifications are not sent for any errors that occur when starting or shutting down the application, so it's important to still use an uptime monitoring service in production.

The code for this functionality is in the `sendErrorNotification()` method (in the `cmd/web/errors.go` file) and the email template for the notification is located at `assets/emails/error-notification.tmpl`.

You'll need to make sure that the application is [configured using valid SMTP credentials](#sending-emails) in order to send the email.

## Admin tasks

The `Makefile` in the project root contains commands to easily run common admin tasks:

|     |     |
| --- | --- |
| `$ make tidy` | Format all code using `go fmt` and tidy the `go.mod` file. |
| `$ make audit` | Run `go vet`, `staticheck`, execute all tests and verify required modules. |
| `$ make build` | Build a binary for the `cmd/web` application and store it in the `bin` folder. |
| `$ make run` | Build and then run a binary for the `cmd/web` application (uses live reloading). |

## Live reload

When you use `make run` to run the application, the application will automatically be rebuilt and restarted whenever you make changes to any files with the following extensions:

```
.go
.tpl, .tmpl, .html
.css, .js, .sql
.jpeg, .jpg, .gif, .png, .bmp, .svg, .webp, .ico
```

Behind the scenes the live reload functionality uses the [cosmtrek/air](https://github.com/cosmtrek/air) tool. You can configure how it works (including which file extensions and folders are watched for changes) by editing the `air.toml` file.

## Running background tasks

A `backgroundTask()` helper is included in the `cmd/web/helpers.go` file. You can call this in your handlers, helpers and middleware to run any logic in a separate background goroutine. This useful for things like sending emails, or completing slow-running jobs.

You can call it like so:

```
func (app *application) yourHandler(w http.ResponseWriter, r *http.Request) {
    ...

    app.backgroundTask(func() error {
        // The logic you want to execute in a background task goes here.
        // It should return an error, or nil.
        err := doSomething()
        if err != nil {
            return err
        }

        return nil
    })

    ...
}
```

Using the `backgroundTask()` helper will automatically recover any panics in the background task logic, and when performing a graceful shutdown the application will wait for any background tasks to finish running before it exits.

## Application version

The application version number is generated automatically based on your latest version control system revision number. If you are using Git, this will be your latest Git commit hash. It can be retrieved by calling the `version.Get()` function from the `internal/version` package.

Important: The version control system revision number will only be available when the application is built using `go build`. If you run the application using `go run` then `version.Get()` will return the string `"unavailable"`.

## Changing the module path

The module path is currently set to `pks.pyfreebilling.com`. If you want to change this please find and replace all instances of `pks.pyfreebilling.com` in the codebase with your own module path.