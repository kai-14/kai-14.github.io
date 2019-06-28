var returnedData = [];
function myCBFunction(jsonpData) {
    //Loop though the jsonpData object and push the elements onto the returnedData array.
    for(var i = 0; i < jsonpData.WIP2.length; i++) {
        returnedData.push({
            "Batch_Name":jsonpData.WIP2[i].Batch_Name,
            "Batch_Notes":jsonpData.WIP2[i].Batch_Notes,
            "Client_Batch":jsonpData.WIP2[i].Client_Batch,
            "Client_ID":jsonpData.WIP2[i].Client_Batch,
            "Date_Accessioned": jsonpData.WIP2[i].Date_Accessioned,
            "Date_Iso_Completed":jsonpData.WIP2[i].Date_Iso_Completed,
            "Date_Iso_Started": jsonpData.WIP2[i].Date_Iso_Started,
            "Date_Off_Hold": jsonpData.WIP2[i].Date_Off_Hold,
            "Date_QC_Completed": jsonpData.WIP2[i].Date_QC_Completed,
            "Date_QC_Started":jsonpData.WIP2[i].Date_QC_Started,
            "Downstream":jsonpData.WIP2[i].Downstream,
            "Due_By": jsonpData.WIP2[i].Due_By,
            "From_Iso":jsonpData.WIP2[i].From_Iso,
            "High_Priority":jsonpData.WIP2[i].High_Priority,
            "ID":jsonpData.WIP2[i].ID,
            "ID_str": jsonpData.WIP2[i].ID_str,
            "IsoCode":jsonpData.WIP2[i].IsoCode,
            "Iso_Comp_NA":jsonpData.WIP2[i].Iso_Comp_NA,
            "Iso_Notes":jsonpData.WIP2[i].Iso_Notes,
            "Iso_Start_NA":jsonpData.WIP2[i].Iso_Start_NA,
            "Iso_Type_String":jsonpData.WIP2[i].Iso_Type_String,
            "Isolation_Type":jsonpData.WIP2[i].Isolation_Type,
            "Low_Conc":jsonpData.WIP2[i].Low_Conc,
            "Low_DV200":jsonpData.WIP2[i].Low_DV200,
            "Low_RINs":jsonpData.WIP2[i].Low_RINs,
            "Low_Yields": jsonpData.WIP2[i].Low_Yields,
            "MW_HM_KS_Notes": jsonpData.WIP2[i].MW_HM_KS_Notes,
            "Methods": jsonpData.WIP2[i].Methods,
            "Multiple_Shipments":jsonpData.WIP2[i].Multiple_Shipments,
            "Number_of_Samples":jsonpData.WIP2[i].Number_of_Samples,
            "On_Hold":jsonpData.WIP2[i].On_Hold,
            "Overall_Expected_Completion_Date":jsonpData.WIP2[i].Overall_Expected_Completion_Date,
            "PMs1":jsonpData.WIP2[i].PMs1,
            "Prep_Category": jsonpData.WIP2[i].Prep_Category,
            "QC_Comp_NA":jsonpData.WIP2[i].QC_Comp_NA,
            "QC_Notes":jsonpData.WIP2[i].QC_Notes,
            "QC_Start_NA": jsonpData.WIP2[i].QC_Start_NA,
            "Sample_Request_Number_s": jsonpData.WIP2[i].Sample_Request_Number_s,
            "Sample_Type": jsonpData.WIP2[i].Sample_Type,
            "Sample_Type_String":jsonpData.WIP2[i].Sample_Type_String,
            "Status": jsonpData.WIP2[i].Status,
            "Task_Type":jsonpData.WIP2[i].Task_Type,
            "Tissue_Info": jsonpData.WIP2[i].Tissue_Info,
            "Upcoming_Dates_for_this_Iso_Type":jsonpData.WIP2[i].Upcoming_Dates_for_this_Iso_Type
        });
}};


(function() {
    // Create the connector object
    var myConnector = tableau.makeConnector();
    // Define the schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [{
            id: "Batch_Name",
            dataType: tableau.dataTypeEnum.string
            }, {
            id: "Batch_Notes",
            dataType: tableau.dataTypeEnum.string
            }, {
            id: "Client_Batch",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Client_ID",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_Accessioned",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_Iso_Completed",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_Iso_Started",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_Off_Hold",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_QC_Completed",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Date_QC_Started",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Downstream",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Due_By",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"From_Iso",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"High_Priority",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"ID",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"ID_str",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"IsoCode",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Iso_Comp_NA",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Iso_Notes",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Iso_Start_NA",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Iso_Type_String",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Isolation_Type",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Low_Conc",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Low_DV200",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Low_RINs",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Low_Yields",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"MW_HM_KS_Notes",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Methods",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Multiple_Shipments",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Number_of_Samples",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"On_Hold",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Overall_Expected_Completion_Date",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"PMs1",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Prep_Category",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"QC_Comp_NA",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"QC_Notes",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"QC_Start_NA",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Sample_Request_Number_s",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Sample_Type",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Sample_Type_String",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Status",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Task_Type",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Tissue_Info",
            dataType: tableau.dataTypeEnum.string
            }, {
            id:"Upcoming_Dates_for_this_Iso_Type",
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
scriptTag.src = "https://creator.zoho.com/api/json/iso-qc-schedule/view/WIP_Extract?authtoken="+window.location.search.substr(1)+"&scope=creatorapi&zc_ownername=q2labsolutions&callback=myCBFunction";
document.getElementsByTagName('head')[0].appendChild(scriptTag);
    // Create event listeners for when the user submits the form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Zoho Creator Iso-QC WIP Data"; // This will be the data source name in Tableau
            tableau.submit(); // This sends the connector object to Tableau
        });
    });
})();

