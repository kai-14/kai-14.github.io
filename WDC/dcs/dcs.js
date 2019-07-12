var returnedData = [];

function myCBFunction(jsonpData) {
	//console.log(jsonpData.Create_Ticket[0]);
	//Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.Create_Ticket.length; i++) {
        returnedData.push({
        "Additional_Information": jsonpData.Create_Ticket[i].Additional_Information,
        "Additional_Reviewers_Beyond_Those_Required": jsonpData.Create_Ticket[i].Additional_Reviewers_Beyond_Those_Required,
        "Complete_Status_Date":jsonpData.Create_Ticket[i].Additional_Reviewers_Beyond_Those_Required,
        "DCRs_to_Address": jsonpData.Create_Ticket[i].DCRs_to_Address,
        "Date_Ticket_Completed":jsonpData.Create_Ticket[i].Date_Ticket_Completed,
        "Date_Ticket_Submitted": jsonpData.Create_Ticket[i].Date_Ticket_Submitted,
        "Date_of_Project_Status_Change": jsonpData.Create_Ticket[i].Date_of_Project_Status_Change,
        "Document_Effective_Date":jsonpData.Create_Ticket[i].Document_Effective_Date,
        "Document_ID":jsonpData.Create_Ticket[i].Document_ID,
        "Email": jsonpData.Create_Ticket[i].Email,
        "Functional_Area_Manager": jsonpData.Create_Ticket[i].Functional_Area_Manager,
        "Have_DCRs_Been_Addressed": jsonpData.Create_Ticket[i].Have_DCRs_Been_Addressed,
        "Have_reviewer_comments_been_addressed": jsonpData.Create_Ticket[i].Have_reviewer_comments_been_addressed,
        "High_Priority":jsonpData.Create_Ticket[i].High_Priority,
        "ID":jsonpData.Create_Ticket[i].ID,
        "Medical_Writer_Assigned": jsonpData.Create_Ticket[i].Medical_Writer_Assigned,
        "Name": jsonpData.Create_Ticket[i].Name,
        "OverallTAT":jsonpData.Create_Ticket[i].OverallTAT,
        "PendingCompleteTAT":jsonpData.Create_Ticket[i].PendingCompleteTAT,
        "Pending_Status_Date": jsonpData.Create_Ticket[i].Pending_Status_Date,
        "Project_Anticipated_Completion_Date":jsonpData.Create_Ticket[i].Project_Anticipated_Completion_Date,
        "Project_Category": jsonpData.Create_Ticket[i].Project_Category,
        "Project_Status": jsonpData.Create_Ticket[i].Project_Status,
        "Rejected_Status_Date":jsonpData.Create_Ticket[i].Rejected_Status_Date,
        "Requested_Due_Date":jsonpData.Create_Ticket[i].Requested_Due_Date,
        "Required_Changes":jsonpData.Create_Ticket[i].Required_Changes,
        "SubmitPendingTAT": jsonpData.Create_Ticket[i].SubmitPendingTAT,
        "Submit_Date":jsonpData.Create_Ticket[i].Submit_Date,
        "Ticket_Number":jsonpData.Create_Ticket[i].Ticket_Number,
        "Writer_Comments":jsonpData.Create_Ticket[i].Writer_Comments,
        "Your_QID":jsonpData.Create_Ticket[i].Your_QID,
        "eSOP_Link":jsonpData.Create_Ticket[i].eSOP_Link
        });
    }};


(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();

    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "Additional_Information",
            dataType: tableau.dataTypeEnum.string
        }, {
            id: "Additional_Reviewers_Beyond_Those_Required",
            dataType: tableau.dataTypeEnum.string
        }, {
                id: "Complete_Status_Date", dataType: tableau.dataTypeEnum.date
            }, {
                id: "DCRs_to_Address", dataType: tableau.dataTypeEnum.string
            },{
                id: "Date_Ticket_Completed", dataType: tableau.dataTypeEnum.date
            },{
                id: "Date_Ticket_Submitted", dataType: tableau.dataTypeEnum.date
            },{
                id: "Date_of_Project_Status_Change", dataType: tableau.dataTypeEnum.date
            },{
                id: "Document_Effective_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Document_ID", dataType: tableau.dataTypeEnum.string
            },{
                id: "Email", dataType: tableau.dataTypeEnum.string
            },{
                id: "Functional_Area_Manager", dataType: tableau.dataTypeEnum.string
            },{
                id: "Have_DCRs_Been_Addressed", dataType: tableau.dataTypeEnum.bool
            },{
                id: "Have_reviewer_comments_been_addressed", dataType: tableau.dataTypeEnum.bool
            },{
                id: "High_Priority", dataType: tableau.dataTypeEnum.bool
            },{
                id: "Medical_Writer_Assigned", dataType: tableau.dataTypeEnum.string
            },{
                id: "Name", dataType: tableau.dataTypeEnum.string
            },{
                id: "OverallTAT", dataType: tableau.dataTypeEnum.float
            },{
                id: "PendingCompleteTAT", dataType: tableau.dataTypeEnum.float
            },{
                id: "Pending_Status_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Project_Anticipated_Completion_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Project_Category", dataType: tableau.dataTypeEnum.string
            },{
                id: "Project_Status", dataType: tableau.dataTypeEnum.string
            },{
                id: "Rejected_Status_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Requested_Due_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Required_Changes", dataType: tableau.dataTypeEnum.string
            },{
                id: "SubmitPendingTAT", dataType: tableau.dataTypeEnum.float
            },{
                id: "Submit_Date", dataType: tableau.dataTypeEnum.date
            },{
                id: "Ticket_Number", dataType: tableau.dataTypeEnum.int
            },{
                id: "Writer_Comments", dataType: tableau.dataTypeEnum.string
            },{
                id: "Your_QID", dataType: tableau.dataTypeEnum.string
            },{
                id: "eSOP_Link", dataType: tableau.dataTypeEnum.string
            }];

        var tableSchema = {
            id: "zohoFeed",
            alias: "Zoho Data from Doc Ctl Support",
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
scriptTag.src = "https://creator.zoho.com/api/json/document-control-support/view/DCS_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Document Control Support"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();