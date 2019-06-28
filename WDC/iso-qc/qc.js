var returnedData = [];

function myCBFunction(jsonpData) {
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.QC_Details.length; i++) {
        returnedData.push({
            "ID_str": jsonpData.QC_Details[i].ID_str,
            "Batch_Database_ID":jsonpData.QC_Details[i].Batch_Database_ID,
            "Equipment": jsonpData.QC_Details[i].Equipment,
            "ID": jsonpData.QC_Details[i].ID,
            "Note": jsonpData.QC_Details[i].Note,
            "QC_Date": jsonpData.QC_Details[i].QC_Date,
            "Qty_Samples": jsonpData.QC_Details[i].Qty_Samples
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
            id: "Batch_Database_ID",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Equipment",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "ID",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Note",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "QC_Date",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Qty_Samples",
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
scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/QC_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator QC Subform Data"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();

