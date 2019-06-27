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
	console.log(jsonpData.Add_Shipment[0].ID_str);
	//Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Add_Shipment.length; i++) {
        returnedData.push({
            "ID_str": jsonpData.Add_Shipment[i].ID_str,
            "Client Batch": jsonpData.Add_Shipment[i].Client_Batch,
            "Number_of_Samples": jsonpData.Add_Shipment[i].Number_of_Samples,
		"Accessioner": jsonpData.Add_Shipment[i].Accessioner,
"Additional_Accessioner_search_1":jsonpData.Add_Shipment[i].Additional_Accessioner_search_1,
"Additional_Accessioner_search_2":jsonpData.Add_Shipment[i].Additional_Accessioner_search_2,
"Additional_Accessioner_search_3":jsonpData.Add_Shipment[i].Additional_Accessioner_search_3,
"Additional_Container_Type_1":jsonpData.Add_Shipment[i].Additional_Container_Type_1,
"Additional_PM_search_1":jsonpData.Add_Shipment[i].Additional_PM_search_1,
"Additional_PM_search_2":jsonpData.Add_Shipment[i].Additional_PM_search_2,
"Additional_PM_search_3":jsonpData.Add_Shipment[i].Additional_PM_search_3,
"Additional_Received_By_search_1":jsonpData.Add_Shipment[i].Additional_Received_By_search_1,
"Additional_Received_By_search_2":jsonpData.Add_Shipment[i].Additional_Received_By_search_2,
"Additional_Received_By_search_3":jsonpData.Add_Shipment[i].Additional_Received_By_search_3,
"Additional_Sales_search_1":jsonpData.Add_Shipment[i].Additional_Sales_search_1,
"Additional_Sales_search_2":jsonpData.Add_Shipment[i].Additional_Sales_search_2,
"Aliquot_Type":jsonpData.Add_Shipment[i].Aliquot_Type,
"Arrival_Condition":jsonpData.Add_Shipment[i].Arrival_Condition,
"Arrival_Email":jsonpData.Add_Shipment[i].Arrival_Email,
"Arrived_Set_Up":jsonpData.Add_Shipment[i].Arrived_Set_Up,
"Auto_Number":jsonpData.Add_Shipment[i].Auto_Number,
"Batch":jsonpData.Add_Shipment[i].Batch,
"Batch_Accessioned":jsonpData.Add_Shipment[i].Batch_Accessioned,
"Batch_Ready":jsonpData.Add_Shipment[i].Batch_Ready,
"Batch_Set_Up":jsonpData.Add_Shipment[i].Batch_Set_Up,
"Batch_TAT":jsonpData.Add_Shipment[i].Batch_TAT,
"Check":jsonpData.Add_Shipment[i].Check,
"Client":jsonpData.Add_Shipment[i].Client,
"Container_Type":jsonpData.Add_Shipment[i].Container_Type,
"Courier":jsonpData.Add_Shipment[i].Courier,
"Data_Logger":jsonpData.Add_Shipment[i].Data_Logger,
"Data_Logger_Received":jsonpData.Add_Shipment[i].Data_Logger_Received,
"Days_Since_Arrival":jsonpData.Add_Shipment[i].Days_Since_Arrival,
"Discrepancy":jsonpData.Add_Shipment[i].Discrepancy,
"Disposition":jsonpData.Add_Shipment[i].Disposition,
"Expected":jsonpData.Add_Shipment[i].Expected,
"Expected_Accession_Date":jsonpData.Add_Shipment[i].Expected_Accession_Date,
"File_upload":jsonpData.Add_Shipment[i].File_upload,
"Hand_written_IDs":jsonpData.Add_Shipment[i].Hand_written_IDs,
"High_Priority":jsonpData.Add_Shipment[i].High_Priority,
"ID_Mismatch":jsonpData.Add_Shipment[i].ID_Mismatch,
"Isolation_Type":jsonpData.Add_Shipment[i].Isolation_Type/*,
"Last_Contact":jsonpData.Add_Shipment[i].Last_Contact,
"Manifest_not_Provided":jsonpData.Add_Shipment[i].Manifest_not_Provided,
"Notes":jsonpData.Add_Shipment[i].Notes,
"Notified_Esoteric":jsonpData.Add_Shipment[i].Notified_Esoteric,
"Number_of_Samples":jsonpData.Add_Shipment[i].Number_of_Samples,
"Number_of_Slides":jsonpData.Add_Shipment[i].Number_of_Slides,
"Other_Discrepancy":jsonpData.Add_Shipment[i].Other_Discrepancy,
"PM_Form":jsonpData.Add_Shipment[i].PM_Form,
"Quote":jsonpData.Add_Shipment[i].Quote,
"Ready_Accessioned_TAT":jsonpData.Add_Shipment[i].Ready_Accessioned_TAT,
"Received_Accessioned_TAT":jsonpData.Add_Shipment[i].Received_Accessioned_TAT,
"Received_By":jsonpData.Add_Shipment[i].Received_By,
"Received_Date":jsonpData.Add_Shipment[i].Received_Date,
"Received_Ready_TAT":jsonpData.Add_Shipment[i].Received_Ready_TAT,
"SSF_Not_Submitted":jsonpData.Add_Shipment[i].SSF_Not_Submitted,
"Sales_Form":jsonpData.Add_Shipment[i].Sales_Form,
"Sent_to_Iso":jsonpData.Add_Shipment[i].Sent_to_Iso,
"Service_Type":jsonpData.Add_Shipment[i].Service_Type,
"Status_Reason":jsonpData.Add_Shipment[i].Status_Reason,
"Status_of_Batch":jsonpData.Add_Shipment[i].Status_of_Batch,
"Tracking":jsonpData.Add_Shipment[i].Tracking*/
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
        }, {
		id:"Accessioner",
		alias: "Accessioner",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Accessioner_search_1",
		dataType: tableau.dataTypeEnum.string

	}, {
		id: "Additional_Accessioner_search_2",
		dataType: tableau.dataTypeEnum.string

	}, {
		id: "Additional_Accessioner_search_3",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Container_Type_1",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_PM_search_1",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_PM_search_2",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_PM_search_3",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Received_By_search_1",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Received_By_search_2",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Received_By_search_3",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Sales_search_1",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Additional_Sales_search_2",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Aliquot_Type",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Arrival_Condition",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Arrival_Email",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Arrived_Set_Up",
		dataType: tableau.dataTypeEnum.bool
    }, {
        id: "Auto_Number",
        dataType: tableau.dataTypeEnum.int
    }, {
		id: "Batch",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Batch_Accessioned",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Batch_Ready",
		dataType: tableau.dataTypeEnum.datetime
	}, {
		id: "Batch_Set_Up",
		dataType: tableau.dataTypeEnum.datetime
	}, {
		id: "Batch_TAT",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Check",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Client",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Container_Type",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Courier",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Data_Logger",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Data_Logger_Received",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Days_Since_Arrival",
		dataType: tableau.dataTypeEnum.float
	}, {
		id: "Discrepancy",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Disposition",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Expected",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Expected_Accession_Date",
		dataType: tableau.dataTypeEnum.datetime
	}, {
		id: "File_upload",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Hand_written_IDs",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "High_Priority",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "ID_Mismatch",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Isolation_Type",
		dataType: tableau.dataTypeEnum.string
	}/*, {
		id: "Last_Contact",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Manifest_not_Provided",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Notes",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Notified_Esoteric",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Number_of_Samples",
		dataType: tableau.dataTypeEnum.int
	}, {
		id: "Number_of_Slides",
		dataType: tableau.dataTypeEnum.int
	}, {
		id: "Other_Discrepancy",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "PM_Form",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Quote",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Ready_Accessioned_TAT",
		dataType: tableau.dataTypeEnum.float
	}, {
		id: "Received_Accessioned_TAT",
		dataType: tableau.dataTypeEnum.float
	}, {
		id: "Received_By",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Received_Date",
		dataType: tableau.dataTypeEnum.datetime
	}, {
		id: "Received_Ready_TAT",
		dataType: tableau.dataTypeEnum.float
	}, {
		id: "SSF_Not_Submitted",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Sales_Form",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Sent_to_Iso",
		dataType: tableau.dataTypeEnum.bool
	}, {
		id: "Service_Type",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Status_Reason",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Status_of_Batch",
		dataType: tableau.dataTypeEnum.string
	}, {
		id: "Tracking",
		dataType: tableau.dataTypeEnum.string
    }*/];

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