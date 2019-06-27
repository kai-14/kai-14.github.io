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
    for(var i = 0; i < jsonpData.WIP2.length; i++) {
        returnedData.push({
            "ID_str": jsonpData.WIP2[i].ID_str,
            "Client Batch": jsonpData.WIP2[i].Client_Batch,
            "Number_of_Samples": jsonpData.WIP2[i].Number_of_Samples
        });
/*
Batch_Name: "2019-05-29_GO29505_28233"
Batch_Notes: "remove OCT and carve out tissue; Holding for more clarification on batch. HMM 30May2019"
Client_Batch: "EA16113 - (2019-05-29_GO29505_28233)"
Client_ID: "EA16113"
Date_Accessioned: "29-May-2019"
Date_Iso_Completed: ""
Date_Iso_Started: ""
Date_Off_Hold: ""
Date_QC_Completed: ""
Date_QC_Started: ""
Downstream: ""
Due_By: ""
From_Iso: ""
High_Priority: true
ID: 3434202000004281300
ID_str: "3434202000004281441"
IsoCode: ""
Iso_Comp_NA: false
Iso_Notes: ""
Iso_Start_NA: false
Iso_Type_String: " - "
Isolation_Type: ""
Low_Conc: ""
Low_DV200: ""
Low_RINs: ""
Low_Yields: ""
MW_HM_KS_Notes: ""
Methods: "[]"
Multiple_Shipments: ""
Number_of_Samples: 27
On_Hold: true
Overall_Expected_Completion_Date: ""
PMs1: "[Allen Clayton]"
Prep_Category: ""
QC_Comp_NA: false
QC_Notes: ""
QC_Start_NA: false
Sample_Request_Number_s: ""
Sample_Type: "[]"
Sample_Type_String: ""
Status: "Iso+QC"
Task_Type: ""
Tissue_Info: ""
Upcoming_Dates_for_this_Iso_Type: ""
*/

}};


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

