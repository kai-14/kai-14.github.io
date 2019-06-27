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
    console.log(jsonpData);
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Add_Shipment.length; i++) {
        returnedData.push({
            "ID": jsonpData.Collector[i].ID_str,
            "Client Batch": jsonpData.Collector[i].Client_Batch,
            "Number_of_Samples": jsonpData.Collector[i].Number_of_Samples
/*
Batch: "2017-11-17_015805_25629"
Batch_Complete: "20-Dec-2017"
ClientID_BatchName: "EA17062_2017-11-17_015805_25629"
Client_Expected_Ship_Date: ""
Client_ID1: "EA17062"
Client_Request: ""
Client_Study_Project_ID: ""
Comments: ""
Completed_By1: "CJD"
Courier: "FedEx"
Days_Post_BC: ""
Disposition: "Return"
Disposition_Complete: "04-Jun-2019 13:54:58"
Expected_vs_Confirmed: "Confirmed Ship Date"
File_upload: false
Final_Disposition: "Return"
Gathered_By: "CJD"
High_Priority: false
ID: 3434202000004103000
Initiated_By1: "CJD"
Initiated_Date: "24-May-2019"
Initiated_Ship_TAT: 11
Manager_Approval_Notes: ""
Multi_Batch_Disposition1: ""
PM: ""
PM_Comments: ""
PM_List: "[Anthony Wrisbon]"
Plates: ""
Quote: "25629"
Remaining_Samples: false
Sample_Type: ""
Samples: 54
Samples_Pulled: "03-Jun-2019 14:11:52"
Ship_Date: "04-Jun-2019"
Shipment_Details: ""
Single_Line: ""
Single_Line1: ""
Special_Return_other: ""
Status: "Complete"
Third_Party_Client: false
Tubes: 48
TubesAndPlates: 48
Verified: "04-Jun-2019 11:25:22"
Verifier1: "DK"
*/



        });
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
scriptTag.src = "https://creator.zoho.com/api/json/disposition-log/view/Collector_Extract?authtoken=fa31ac8ec098f8276c445d5ffdafdf4a&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Dispositions App"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();

