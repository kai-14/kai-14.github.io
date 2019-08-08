var returnedData = [];

function myCBFunction(jsonpData) {
	//Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Add_Shipment.length; i++) {
        returnedData.push({
        	"ID_str": jsonpData.Add_Shipment[i].ID_str,
			"Accessioner": jsonpData.Add_Shipment[i].Accessioner,
			
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
			id:"Accessioner",
			alias: "Accessioner",
			dataType: tableau.dataTypeEnum.string
		}];

        var tableSchema = {
            id: "zohoFeed",
            alias: "Zoho Data from Clarity Mapping",
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
scriptTag.src = "https://creator.zoho.com/api/json/accessioning-log/view/Add_Shipment_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Accessioning Log"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();