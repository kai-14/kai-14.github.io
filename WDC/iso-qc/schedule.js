//var scriptTag = document.createElement('script');
//scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/WIP_Extract?authtoken=fa31ac8ec098f8276c445d5ffdafdf4a&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
//document.getElementsByTagName('head')[0].appendChild(scriptTag);
/*
function myCBFunction(jsonpData) {
    for(var i = 0; i < jsonpData.WIP2.length; i++) {
//        x = BigInt(jsonpData.WIP2[i].ID_str).toString(16);
        console.log(jsonpData.WIP2[i].ID_str);
//        console.log(x);
    }
}
*/
var returnedData = [];

function myCBFunction(jsonpData) {
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    console.log(jsonpData);
//    for(var i = 0; i < jsonpData.Schedule.length; i++) {
 //       returnedData.push({
           /* "ID_str": jsonpData.Schedule[i].ID_str,
}/*);
Calendar_Title: "null - 2019-05-07_GO29527_28699"
Client_Batch: "EA192042 - (2019-05-07_GO29527_28699)"
Date_field: "12-Jun-2019"
Hood: ""
Hood_Location: ""
ID: 3434202000004302300
IsoCode: ""
Mark_for_Deletion: false
Note: ""
Staff: ""
Staff_Email_String: ""
Task_Type: "Iso"
Thermomixers: "[]"
Thermomixers_Formula: ""
WIP1: "3434202000004140366"
*/

//}};


(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "ID_str",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Client_Batch",
            alias: "Client Batch",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Number_of_Samples",
            alias: "Number of Samples",
            dataType: tableau.dataTypeEnum.float
        }];

        var tableSchema = {
            id: "zohoFeed",
            alias: "Zoho Data from Iso-QC",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    myConnector.getData = function(table, doneCallback) {

        table.appendRows(returnedData);
   
        doneCallback();
   
   };
   
   tableau.registerConnector(myConnector);

    /* Download the data
    myConnector.getData = function(table, doneCallback) {
        $.getJSON("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson", function(resp) {
            var feat = resp.features,
                tableData = [];

            // Iterate over the JSON object
            for (var i = 0, len = feat.length; i < len; i++) {
                tableData.push({
                    "id": feat[i].id,
                    "mag": feat[i].properties.mag,
                    "title": feat[i].properties.title,
                    "location": feat[i].geometry
                });
            }

            table.appendRows(tableData);
            doneCallback();
        });
    };

    tableau.registerConnector(myConnector);*/
var scriptTag = document.createElement('script');
scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/Schedule_Extract?authtoken=fa31ac8ec098f8276c445d5ffdafdf4a&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Iso-QC Schedule App"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();