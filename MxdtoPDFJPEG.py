import arcpy, os

arcpy.SetLogHistory(False)

mxd_list = arcpy.GetParameterAsText(0).split(";")
save_folder = arcpy.GetParameterAsText(1)
naming_layer = arcpy.GetParameterAsText(2)
naming_field = arcpy.GetParameterAsText(3)
resolution = int(arcpy.GetParameterAsText(4))
include_geo_data = arcpy.GetParameterAsText(5)
export_as_pdf = arcpy.GetParameterAsText(6)
export_as_jpeg = arcpy.GetParameterAsText(7)
list_length = len(mxd_list)


def printDDPWithNames(mxd):
    page_count = mxd.dataDrivenPages.pageCount
    for pageNum in range(1, page_count+1):
        mxd.dataDrivenPages.currentPageID = pageNum
        if export_as_pdf:
            pdf_name = mxd.dataDrivenPages.pageRow.getValue(naming_field) + ".pdf"
            save_path = os.path.join(save_folder, pdf_name)
            arcpy.AddMessage(r"Exporting " + str(save_path))
            arcpy.mapping.ExportToPDF(mxd, save_path, resolution=resolution, georef_info=include_geo_data, convert_markers=True)
        if export_as_jpeg:
            for i in range(1, mxd.dataDrivenPages.pageCount + 1):
                mxd.dataDrivenPages.currentPageID = i
                row = mxd.dataDrivenPages.pageRow
                arcpy.mapping.ExportToJPEG(mxd, os.path.join(save_folder, row.getValue(naming_field) + ".jpg"),
                                           "PAGE_LAYOUT", resolution=resolution)

def printDDP(path_name, mxd):
    if naming_field:
        printDDPWithNames(mxd)
    else:
        arcpy.AddMessage(r"No field name provided. ")
        file_name = os.path.basename(path_name).split('.')[0]
        if export_as_pdf:
            save_path = os.path.join(save_folder, file_name + ".pdf")
            arcpy.AddMessage(r"Exporting " + str(save_path))
            mxd.dataDrivenPages.exportToPDF(save_path, "ALL", "", "PDF_MULTIPLE_FILES_PAGE_INDEX",
                                            resolution=resolution, georef_info=include_geo_data, convert_markers=True)
        if export_as_jpeg:
            arcpy.AddMessage("Exporting Jpeg")
            for i in range(1, mxd.dataDrivenPages.pageCount + 1):
                mxd.dataDrivenPages.currentPageID = i
                arcpy.AddMessage("Page ID: " + str(i))
                arcpy.mapping.ExportToJPEG(mxd, os.path.join(save_folder, file_name + "_" + str(i) + "_of_" +
                                                             str(mxd.dataDrivenPages.pageCount) + ".jpg"),
                                           "PAGE_LAYOUT", resolution=resolution)

def printMxd(path_name, mxd):
    file_name = os.path.basename(path_name).split('.')[0]
    if export_as_pdf:
        save_path = os.path.join(save_folder, file_name + ".pdf")
        arcpy.AddMessage(r"Exporting " + str(save_path))
        arcpy.mapping.ExportToPDF(mxd, save_path, resolution=resolution, georef_info=include_geo_data, convert_markers=True)
    if export_as_jpeg:
        arcpy.mapping.ExportToJPEG(mxd, os.path.join(save_folder, file_name + ".jpg"), "PAGE_LAYOUT", resolution=resolution)

for index, mxd_path in zip(range(0, list_length), mxd_list):
    arcpy.AddMessage("Export As Jpeg: " + str(export_as_jpeg))
    arcpy.AddMessage("Export As Pdf: " + str(export_as_pdf))
    current_mxd = arcpy.mapping.MapDocument(str(mxd_path))
    arcpy.AddMessage(r"Exporting " + str(index+1) + " of " + str(list_length) + " mxds. ")
    if hasattr(current_mxd, "dataDrivenPages"):
        printDDP(mxd_path, current_mxd)
    else:
        printMxd(mxd_path, current_mxd)

del mxd_list
