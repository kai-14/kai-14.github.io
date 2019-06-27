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
    for(var i = 0; i < jsonpData.Add_Shipment.length; i++) {
        returnedData.push({
            "ID": jsonpData.Add_Shipment[i].ID_str,
            "Client Batch": jsonpData.Add_Shipment[i].Client_Batch,
            "Number_of_Samples": jsonpData.Add_Shipment[i].Number_of_Samples

/*Accessioner: "CAR"
Additional_Accessioner_search_1: ""
Additional_Accessioner_search_2: ""
Additional_Accessioner_search_3: ""
Additional_Container_Type_1: ""
Additional_PM_search_1: ""
Additional_PM_search_2: ""
Additional_PM_search_3: ""
Additional_Received_By_search_1: ""
Additional_Received_By_search_2: ""
Additional_Received_By_search_3: ""
Additional_Sales_search_1: ""
Additional_Sales_search_2: ""
Aliquot_Type: ""
All_Accessioners: "CAR   "
All_PM: "Hannah Redmond   "
All_Received_By: "AM   "
All_Sales: ""
Arrival_Condition: "Frozen"
Arrival_Email: "24-Apr-2018 00:00:00"
Arrived_Set_Up: false
Auto_Number: 5074
Batch: "2018-04-23_25459_WES12_CA224-020"
Batch_Accessioned: "24-Apr-2018 00:00:00"
Batch_Ready: "24-Apr-2018 00:00:00"
Batch_Set_Up: "23-Apr-2018 00:00:00"
Batch_TAT: "expedited/Hold"
Check: ""
Client: "EA10130"
Comments: "Waiting for Batch set up 11Apr2018 AM; batch is set up, awaiting BMS DTS client manifest for accessioning 13APR2018 CAR"
Container_Type: "Screw Cap Tube"
Container_field: "Screw Cap Tube "
Courier: ""
Data_Logger: ""
Data_Logger_Received: false
Days_Since_Arrival: 146.6
Discrepancy: true
Disposition: ""
Expected: ""
Expected_Accession_Date: ""
File_upload: "http://creator.zoho.com/DownloadFile.do?filepath=/&sharedBy=653663544"
Hand_written_IDs: false
High_Priority: false
ID: "3434202000001222644"
ID_Mismatch: false
Isolation_Type: ""
Last_Contact: "11-Apr-2018 00:00:00"
Manifest_not_Provided: false
Notes: ""
Notified_Esoteric: false
Number_of_Samples: 9
Number_of_Slides: ""
Other_Discrepancy: false
PM_Form: "Hannah Redmond"
Quote: "25459"
Ready_Accessioned_TAT: 0
Received_Accessioned_TAT: -13
Received_By: "AM"
Received_Date: "11-Apr-2018 00:00:00"
Received_Ready_TAT: 13
SSF_Not_Submitted: true
Sales_Form: ""
Sent_to_Iso: false
Service_Type: ""
Single_Line: ""
Single_Line1: ""
Status_Reason: ""
Status_of_Batch: "Complete"
Tracking: "536298611687"

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
scriptTag.src = "https://creator.zoho.com/api/json/accessioning-log/view/Add_Shipment_Extract?authtoken=fa31ac8ec098f8276c445d5ffdafdf4a&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Iso-QC Schedule App"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();

