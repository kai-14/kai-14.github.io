var returnedData = [];

function myCBFunction(jsonpData) {
    console.log(jsonpData);
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Collector.length; i++) {
        returnedData.push({
			"Batch": jsonpData.Collector[i].Batch,
			"Batch_Complete": jsonpData.Collector[i].Batch_Complete,
			"ClientID_BatchName": jsonpData.Collector[i].ClientID_BatchName,
			"Client_Expected_Ship_Date": jsonpData.Collector[i].Client_Expected_Ship_Date,
			"Client_ID1": jsonpData.Collector[i].Client_ID1,
			"Client_Request": jsonpData.Collector[i].Client_Request,
			"Client_Study_Project_ID":  jsonpData.Collector[i].Client_Study_Project_ID,
			"Comments": jsonpData.Collector[i].Comments,
			"Completed_By1":  jsonpData.Collector[i].Completed_By1,
			"Courier":  jsonpData.Collector[i].Courier,
			"Days_Post_BC": jsonpData.Collector[i].Days_Post_BC,
			"Disposition": jsonpData.Collector[i].Disposition,
			"Disposition_Complete": jsonpData.Collector[i].Disposition_Complete,
			"Expected_vs_Confirmed":  jsonpData.Collector[i].Expected_vs_Confirmed,
			"File_upload":  jsonpData.Collector[i].File_upload,
			"Final_Disposition": jsonpData.Collector[i].Final_Disposition,
			"Gathered_By":  jsonpData.Collector[i].Gathered_By,
			"High_Priority":  jsonpData.Collector[i].High_Priority,
			"ID_str":  jsonpData.Collector[i].ID_str,
			"Initiated_By1": jsonpData.Collector[i].Initiated_By1,
			"Initiated_Date": jsonpData.Collector[i].Initiated_Date,
			"Initiated_Ship_TAT": jsonpData.Collector[i].Initiated_Ship_TAT,
			"Manager_Approval_Notes": jsonpData.Collector[i].Manager_Approval_Notes,
			"Multi_Batch_Disposition1": jsonpData.Collector[i].Multi_Batch_Disposition1,
			"PM": jsonpData.Collector[i].PM,
			"PM_Comments": jsonpData.Collector[i].PM_Comments,
			"PM_List": jsonpData.Collector[i].PM_List,
			"Plates":  jsonpData.Collector[i].Plates,
			"Quote":  jsonpData.Collector[i].Quote,
			"Remaining_Samples": jsonpData.Collector[i].Remaining_Samples,
			"Sample_Type":  jsonpData.Collector[i].Sample_Type,
			"Samples":  jsonpData.Collector[i].Samples,
			"Samples_Pulled":  jsonpData.Collector[i].Samples_Pulled,
			"Ship_Date":  jsonpData.Collector[i].Ship_Date,
			"Shipment_Details":  jsonpData.Collector[i].Shipment_Details,
			"Single_Line": jsonpData.Collector[i].Single_Line,
			"Single_Line1":  jsonpData.Collector[i].Single_Line1,
			"Special_Return_other": jsonpData.Collector[i].Special_Return_other,
			"Status":  jsonpData.Collector[i].Status,
			"Third_Party_Client":  jsonpData.Collector[i].Third_Party_Client,
			"Tubes": jsonpData.Collector[i].Tubes,
			"TubesAndPlates":  jsonpData.Collector[i].TubesAndPlates,
			"Verified":  jsonpData.Collector[i].Verified,
			"Verifier1":  jsonpData.Collector[i].Verifier1
        });
}};


(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id:"Batch",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Batch_Complete",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"ClientID_BatchName",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Client_Expected_Ship_Date",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Client_ID1",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Client_Request",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Client_Study_Project_ID",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Comments",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Completed_By1",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Courier",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Days_Post_BC",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Disposition",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Disposition_Complete",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Expected_vs_Confirmed",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"File_upload",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Final_Disposition",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Gathered_By",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"High_Priority",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"ID_str",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Initiated_By1",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Initiated_Date",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Initiated_Ship_TAT",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Manager_Approval_Notes",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Multi_Batch_Disposition1",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"PM",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"PM_Comments",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"PM_List",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Plates",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Quote",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Remaining_Samples",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Sample_Type",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Samples",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Samples_Pulled",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Ship_Date",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Shipment_Details",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Single_Line",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Single_Line1",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Special_Return_other",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Status",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Third_Party_Client",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Tubes",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"TubesAndPlates",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Verified",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Verifier1",
			dataType: tableau.dataTypeEnum.string
		}];

        var tableSchema = {
            id: "zohoFeed",
            alias: "Zoho Data from Disposition Log",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    myConnector.getData = function(table, doneCallback) {
        table.appendRows(returnedData);
        doneCallback();
   };
   
   tableau.registerConnector(myConnector);

var scriptTag = document.createElement('script');
scriptTag.src = "https://creator.zoho.com/api/json/disposition-log/view/Collector_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Dispositions App"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();