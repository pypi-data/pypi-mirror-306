//Pine Apple db AUTHER BY CIBER CLEANER FACEBOOK:CIBER CLEANER
//configurations
var config = 
{
    "server_url":"http://localhost:81",
    "server_port":"81"

}
//inits

var database_list = document.getElementById("database_list")

//LOADER
var LOADER = document.getElementById('loader');


function showLoader(bool)
{
        LOADER.style.visibility = "visible"

        setTimeout(function() {
            LOADER.style.visibility = "hidden";
        }, 6000);
    
}

function Flask_Client(Method, Host, Data, callback) {

    showLoader(true);
    var client_send = new XMLHttpRequest();
    client_send.open(Method, Host, true);
    client_send.setRequestHeader("Content-Type", "application/json");
 
    client_send.onload = function() {
        if (client_send.status == 200) {
            console.log(client_send.responseText);
            if (callback) {
                showLoader(false);
                callback(null, JSON.parse(client_send.responseText)); // Call the callback with the response
            }
        } else {
            showLoader(false);
            console.log("[🚫] System error detected");
            if (callback) {
                callback(new Error("System error detected: " + client_send.statusText)); // Call the callback with an error
            }
        }
    };

    client_send.onerror = function() {
        console.log("[🚫] Network error detected");
        if (callback) {
            callback(new Error("Network error detected")); // Call the callback with an error
        }
    };

    client_send.send(JSON.stringify(Data));
}
//API CALL CREATED DATABASES
function GETDB()
{

    Flask_Client('GET', config['server_url']+'/api/databases', null, function(error, data) {
        if (error) {
            console.error(error.message);
        } else {
            let db_list_len = data.length;
            for(let rows = 0;rows<db_list_len;rows++)
            {   
                let db_list_card = `<style>
               
    /* this card is inspired form this - https://georgefrancis.dev/ */
    
    .cardx {
      --border-radius: 0.75rem;
      --primary-color: #7257fa;
      --secondary-color: black;
      width: 210px;
      font-family: "Arial";
      padding: 1rem;
      cursor: pointer;
      border-radius: var(--border-radius);
      background: #f1f1f3;
      box-shadow: 0px 8px 16px 0px rgb(0 0 0 / 3%);
      position: relative;
     
    }
    
    .cardx > * + * {
      margin-top: 1.1em;
    }
    
    .cardx .card__content {
      color: var(--secondary-color);
      font-size: 0.86rem;
    }
    
    .cardx .card__title {
      padding: 0;
      font-size: 1.3rem;
      font-weight: bold;
    }
    
    .cardx .card__date {
      color: #6e6b80;
      font-size: 0.8rem;
    }
    
    .cardx .card__arrow {
      position: absolute;
      background: black;
      padding: 0.4rem;
      border-top-left-radius: var(--border-radius);
      border-bottom-right-radius: var(--border-radius);
      bottom: 0;
      right: 0;
      transition: 0.2s;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .cardx svg {
      transition: 0.2s;
    }
    
    /* hover */
    .cardx:hover .card__title {
      color: var(--primary-color);
      text-decoration: none;
    }
    
    .cardx:hover .card__arrow {
      background: #111;
    }
    
    .cardx:hover .card__arrow svg {
      transform: translateX(3px);
    }
      </style>
    <div class="cardx">
        <h3 class="card__title">`+data[rows]['database']+`
        </h3>
        <p class="card__content">Create a database to efficiently store and manage your data.</p>
        <div class="card__date">
           `+data[rows]['datetime']+`
        </div>
        <div class="card__arrow" style="color:white;">
  <a style="color:white;" href="`+config['server_url']+`/dbms/`+data[rows]['database']+`" style="text-decoration: none;">
           <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-database-fill-gear" viewBox="0 0 16 16">
  <path d="M8 1c-1.573 0-3.022.289-4.096.777C2.875 2.245 2 2.993 2 4s.875 1.755 1.904 2.223C4.978 6.711 6.427 7 8 7s3.022-.289 4.096-.777C13.125 5.755 14 5.007 14 4s-.875-1.755-1.904-2.223C11.022 1.289 9.573 1 8 1"/>
  <path d="M2 7v-.839c.457.432 1.004.751 1.49.972C4.722 7.693 6.318 8 8 8s3.278-.307 4.51-.867c.486-.22 1.033-.54 1.49-.972V7c0 .424-.155.802-.411 1.133a4.51 4.51 0 0 0-4.815 1.843A12 12 0 0 1 8 10c-1.573 0-3.022-.289-4.096-.777C2.875 8.755 2 8.007 2 7m6.257 3.998L8 11c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V10c0 1.007.875 1.755 1.904 2.223C4.978 12.711 6.427 13 8 13h.027a4.55 4.55 0 0 1 .23-2.002m-.002 3L8 14c-1.682 0-3.278-.307-4.51-.867-.486-.22-1.033-.54-1.49-.972V13c0 1.007.875 1.755 1.904 2.223C4.978 15.711 6.427 16 8 16c.536 0 1.058-.034 1.555-.097a4.5 4.5 0 0 1-1.3-1.905m3.631-4.538c.18-.613 1.048-.613 1.229 0l.043.148a.64.64 0 0 0 .921.382l.136-.074c.561-.306 1.175.308.87.869l-.075.136a.64.64 0 0 0 .382.92l.149.045c.612.18.612 1.048 0 1.229l-.15.043a.64.64 0 0 0-.38.921l.074.136c.305.561-.309 1.175-.87.87l-.136-.075a.64.64 0 0 0-.92.382l-.045.149c-.18.612-1.048.612-1.229 0l-.043-.15a.64.64 0 0 0-.921-.38l-.136.074c-.561.305-1.175-.309-.87-.87l.075-.136a.64.64 0 0 0-.382-.92l-.148-.045c-.613-.18-.613-1.048 0-1.229l.148-.043a.64.64 0 0 0 .382-.921l-.074-.136c-.306-.561.308-1.175.869-.87l.136.075a.64.64 0 0 0 .92-.382zM14 12.5a1.5 1.5 0 1 0-3 0 1.5 1.5 0 0 0 3 0"/>
</svg>
</a>
        </div>
    </div>`;
    
            database_list.innerHTML += db_list_card
            }
            
            console.log("Received data:", data);
            // You can update your UI or perform other actions here
        }
    });
}

//CREATE DB
function createdb()
{   showLoader(true);
    var dbName = document.getElementById("dbname");
    var database_name = dbName.value;
   
    Flask_Client("POST", config['server_url'] + "/createdb", { "name": database_name }, function(error, responseData) {
        if (error) {
            console.error(error.message);
        } else {
            GETDB();
            console.log("Database created successfully:", responseData);
            // You can perform additional actions here based on the response
        }
    });
    

}




//GET DB LIST ON PAGE LOAD
GETDB();
showLoader(true);