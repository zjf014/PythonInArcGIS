# coding=utf-8
"""
Source code for potential gp tool to create outputs based on attributes
of an input.
"""

import arcpy
import numbers
import sys

try:
    unicode
except:
    unicode = str


def get_unique_values(in_data, fields):
    """
    Identify all unique values for field(s) in a data source

    :param in_data: Input data source
    :param fields: Field name
    :return: A list of unique values
    """

    # Respect extent environment where possible
    if arcpy.env.extent:
        lyr_name = 'sbyloc_extent'
        try:
            lyr = arcpy.MakeFeatureLayer_management(in_data, lyr_name)[0]
            arcpy.SelectLayerByLocation_management(lyr, 'INTERSECT',
                                                   arcpy.env.extent.polygon)
            in_data = lyr_name
        except arcpy.ExecuteError:
            pass
    
    table_name = arcpy.CreateUniqueName('freq', 'in_memory')
    arcpy.Frequency_analysis(in_data, table_name, fields)
    atts = [r for r in arcpy.da.SearchCursor(table_name, fields)]

    try:
        arcpy.Delete_management(table_name)
    except arcpy.ExecuteError:
        # Should delete, but don't fail for intermediate data issues
        pass

    return atts


def create_name(workspace, name, extension):
    """
    Create a unique name

    :param workspace: The workspace that an expected output will be written to
    :param name: Base name of the output (list)
    :param extension: Extension including the leading period
    :return: A unique name, including pathname
    """

    name = u'_'.join([unicode(i) for i in name])

    name = name.replace('"', '')
    name = name.replace("'", "")

    if name == '':  # name of '' validated to ''
        name = 'T'

    validated_name = u'{}{}'.format(
        arcpy.ValidateTableName(name, workspace),
        extension)

    unique_name = arcpy.CreateUniqueName(validated_name, workspace)

    return unique_name


def create_expression(in_data, field_name, value):
    """
    Create a SQL Expression

    :param in_data: Input data source
    :param field_name: The field name that will be queried
    :param value: The value in the field that will be queried for
    :return: SQL expression
    """

    delimited_field = arcpy.AddFieldDelimiters(in_data, field_name)
    if isinstance(value, numbers.Number):
        return u'{} = {}'.format(delimited_field, value)
    elif isinstance(value, type(None)):
        return u'{} IS NULL'.format(delimited_field)
    else:
        return u''' %s = '%s' ''' % ( delimited_field, value.replace("'", "'\'").replace('"', '\"') )


def select(datatype, *args):
    """
    Data type non-specific Select tool handling

    :param datatype: arcpy.Describe datatype keyword
    :param args: arguments for Select/TableSelect tools
    :return:
    """

    feature_data = datatype in ['FeatureClass', 'FeatureLayer']
    tool_name = 'Select' if feature_data else 'TableSelect'
    eval('arcpy.analysis.{}'.format(tool_name))(*args)


def split_by_atts(in_data, out_workspace, fields):
    """
    Split a feature class include a series of feature classes based on
    unique values in a field.

    :param in_data: The input data source
    :param out_workspace: The output workspace that data will be written to
    :param fields: Unique values in these fields will be used to split the data
    :return: A list of output pathnames (output has been created)
    """

    try:
        from itertools import izip
    except ImportError:
        izip = zip

    datatype = arcpy.Describe(in_data).datatype

    unique_values = get_unique_values(in_data, fields)

    workspace_type = arcpy.Describe(out_workspace).datatype

    # If output workspace is a folder add a .shp extension
    extension = ''
    if workspace_type == 'Folder':
        extension = '.shp'


    arcpy.SetProgressor('STEP', '', 0, len(unique_values), 1)

    outputs = list()
    for i in unique_values:
        output = create_name(out_workspace, i, extension)

        expression = u' AND '.join([
            create_expression(in_data, j[0], j[1])
            for j
            in izip(fields, i)])

        select(datatype, in_data, output, expression)
        values_string = u', '.join([unicode(v) for v in i])

        #arcpy.AddIDMessage('INFORMATIVE', 86245, values_string, output)
        
        outputs.append(output)

        arcpy.SetProgressorPosition()

    return outputs


if __name__ == '__main__':
    in_data = arcpy.GetParameterAsText(0)
    out_workspace = arcpy.GetParameterAsText(1)
    fields = [i.value for i in arcpy.GetParameter(2)]

    try:
        split_by_atts(in_data, out_workspace, fields)
        #arcpy.SetParameterAsText(3, out_workspace)
    except Exception as err:
        arcpy.AddError(str(err))
        sys.exit(1)


