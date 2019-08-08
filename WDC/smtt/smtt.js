var returnedData = [];

function myCBFunction(jsonpData) {
	//Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Add_Ticket.length; i++) {
        returnedData.push({
            "Added_Time1": jsonpData.Add_Ticket[i].Added_Time1,
            "Additional_Comments": jsonpData.Add_Ticket[i].Additional_Comments,
            "Additional_SM": jsonpData.Add_Ticket[i].Additional_SM,
            "Attachments": jsonpData.Add_Ticket[i].Attachments,
            "Date_Ticket_Closed": jsonpData.Add_Ticket[i].Date_Ticket_Closed,
            "Date_Time_Needed": jsonpData.Add_Ticket[i].Date_Time_Needed,
            "Description": jsonpData.Add_Ticket[i].Description,
            "Email": jsonpData.Add_Ticket[i].Email,
            "ID": jsonpData.Add_Ticket[i].ID,
            "ID_str": jsonpData.Add_Ticket[i].ID_str,
            "Name": jsonpData.Add_Ticket[i].Name,
            "Pick_Up_Location": jsonpData.Add_Ticket[i].Pick_Up_Location,
            "Priority": jsonpData.Add_Ticket[i].Priority,
            "QID": jsonpData.Add_Ticket[i].QID,
            "Status": jsonpData.Add_Ticket[i].Status,
            "Subject_field": jsonpData.Add_Ticket[i].Subject_field,
            "Ticket_Owner": jsonpData.Add_Ticket[i].Ticket_Owner,
            "Ticket_Type": jsonpData.Add_Ticket[i].Ticket_Type,
            "Turnaround_Time": jsonpData.Add_Ticket[i].Turnaround_Time
});
}};

(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
			id:"Additional_Comments",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Date_Ticket_Closed",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Date_Time_Needed",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Description",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Email",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"ID_str",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Name",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Pick_Up_Location",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Priority",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"QID",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Status",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Subject_field",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Ticket_Owner",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Ticket_Type",
			dataType: tableau.dataTypeEnum.string
		}, {
			id:"Turnaround_Time",
			dataType: tableau.dataTypeEnum.string
		}];

        var tableSchema = {
            id: "zohoFeed",
            alias: "Zoho Data from SMTT",
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
scriptTag.src = "https://creator.zoho.com/api/json/smtt/view/Ticket_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho SMTT Log"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();