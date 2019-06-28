var returnedData = [];

function myCBFunction(jsonpData) {
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    console.log(jsonpData);
    for(var i = 0; i < jsonpData.Schedule.length; i++) {
       returnedData.push({
            "ID_str": jsonpData.Schedule[i].ID_str,
            "Calendar_Title":jsonpData.Schedule[i].Calendar_Title,
            "Client_Batch":jsonpData.Schedule[i].Client_Batch,
            "Date_field": jsonpData.Schedule[i].Date_field,
            "Hood":jsonpData.Schedule[i].Hood,
            "Hood_Location": jsonpData.Schedule[i].Hood_Location,
            "ID":jsonpData.Schedule[i].ID,
            "IsoCode": jsonpData.Schedule[i].IsoCode,
            "Mark_for_Deletion":jsonpData.Schedule[i].Mark_for_Deletion,
            "Note":jsonpData.Schedule[i].Note,
            "Staff":jsonpData.Schedule[i].Staff,
            "Staff_Email_String":jsonpData.Schedule[i].Staff_Email_String,
            "Task_Type": jsonpData.Schedule[i].Task_Type,
            "Thermomixers": jsonpData.Schedule[i].Thermomixers,
            "Thermomixers_Formula":jsonpData.Schedule[i].Thermomixers_Formula,
            "WIP1": jsonpData.Schedule[i].WIP1
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
            id: "Calendar_Title",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Client_Batch",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Date_field",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Hood",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Hood_Location",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "ID",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "IsoCode",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Mark_for_Deletion",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Note",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Staff",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Staff_Email_String",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Task_Type",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Thermomixers",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Thermomixers_Formula",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "WIP1",
            dataType: tableau.dataTypeEnum.string
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

var scriptTag = document.createElement('script');
scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/Schedule_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Iso-QC Schedule Subform Data"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();