# ##################################################################
#
# Copyright 2023 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pooja Chaudhary(pooja.chaudhary@teradata.com)
# Secondary Owner: Pradeep Garre(pradeep.garre@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################

from teradatamlspk.sql.column import Column
from teradataml.dataframe.sql import _SQLColumnExpression

class DataFrameUtils():

    @staticmethod
    def _tuple_to_list(args, arg_name):
        """
        Converts a tuple of string into list of string and multiple list of strings in a tuple
        to list of strings.

        PARAMETERS:
            args: tuple having list of strings or strings.

        EXAMPLES:
            tuple_to_list(args)

        RETURNS:
            list

        RAISES:
            Value error
        """
        if all(isinstance(value, str) for value in args):
            # Accept only strings in tuple.
            res_list = list(args)
        elif len(args) == 1 and isinstance(args[0], list):
            # Accept one list of strings in tuple.
            res_list = args[0]
        else:
            raise ValueError("'{}' argument accepts only strings or one list of strings".format(arg_name))
        return res_list

    @staticmethod
    def _get_columns_from_tuple_args(args, df_columns):
        """
        Converts a tuple of string, column expression or a list of strings/ column expression in a tuple
        to list of strings.

        PARAMETERS:
            args: tuple having list of strings/ column expression, strings or column expression.
            df_columns: list of column names in the DataFrame.

        EXAMPLES:
            _get_columns_from_tuple_args(args, df_columns)

        RETURNS:
            list
        """
        args = args[0] if len(args) == 1 and isinstance(args[0], list) else args
        columns = []
        for arg in args:
            if arg not in df_columns:
                pass
            else:
                arg = arg if isinstance(arg, str) else arg._tdml_column.name
                columns.append(arg)
        return columns
    
    @staticmethod
    def _udf_col_to_tdml_col(col):
        """
        Converts a Column containing UDF expression to teradataml ColumnExpression.

        PARAMETERS:
            col: Column

        EXAMPLES:
           _udf_col_to_tdml_col(col)

        RETURNS:
            ColumnExpression
        """
        from teradatamlspk.sql.utils import _get_tdml_type
        return _SQLColumnExpression(expression=None, udf=col._udf, udf_type=_get_tdml_type(col._udf_type),\
                                    udf_args=col._udf_args, env_name = col._env_name, delimiter= col._delimiter,\
                                    quotechar=col._quotechar, udf_script = col._udf_script)

