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
    for(var i = 0; i < jsonpData.WIP2.length; i++) {
        returnedData.push({
            "identifier1": jsonpData.WIP2[i].ID_str,
            "identifier2": jsonpData.WIP2[i].Client_Batch,
            "identifier3": jsonpData.WIP2[i].Number_of_Samples
        });
}};


(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "identifier1",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "identifier2",
            alias: "identifier2",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "identifier3",
            alias: "identifier3",
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
scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/WIP_Extract?authtoken=fa31ac8ec098f8276c445d5ffdafdf4a&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Iso-QC Schedule App"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();
