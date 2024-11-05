import ast
import os, re
import json
import nbformat
from enum import Enum
from collections import deque, defaultdict
from teradatamlspk.converter.object_types import spark_objects_


combined_attributes = {
    "writeTo": ["overwrite", "overwritePartitions", "using", "tableProperty"],
    "write": ["json", "csv", "parquet", "options", "option", "format", "orc", "partitionBy", "bucketBy"],
    "read": ["csv", "json", "parquet", "format", "orc"],
    "na": "fill"
}

class UserNoteType(Enum):
    NOT_SUPPORTED = 1
    PARTIALLY_SUPPORTED = 2
    NO_ACTION = 3


class UserNote:
    """
    DESCRIPTION:
        Represents an individual user note of Script.
    """
    def __init__(self, start_line_no, end_line_no, object_name, notes, note_type):
        self.start_line_no = start_line_no
        self.end_line_no = end_line_no
        self.object_name = object_name
        self.user_notes = notes
        self.note_type = note_type

    def to_json(self):
        return {
                "Start Line No": self.start_line_no,
                "End Line No": self.end_line_no,
                "Object Name": self.object_name,
                "Notes": self.user_notes,
                "Notification Type": self.note_type.name
                }

class NotebookUserNote:
    """
    DESCRIPTION:
        Represents an individual user note of Notebook.
    """
    def __init__(self, cell_no, start_line_no, end_line_no, object_name, notes, note_type):
        self.cell_no = cell_no
        self.start_line_no = start_line_no
        self.end_line_no = end_line_no
        self.object_name = object_name
        self.user_notes = notes
        self.note_type = note_type

    def to_json(self):
        return {
                "Cell No": self.cell_no,
                "Start Line No": self.start_line_no,
                "End Line No": self.end_line_no,
                "Object Name": self.object_name,
                "Notes": self.user_notes,
                "Notification Type": self.note_type.name
                }

class UserNotes:
    def __init__(self, user_notes):
        """
        DESCRIPTION:
            Represents a list of UserNote objects that are of a given input file
            and provides methods to manipulate and format these notes.

        PARAMETERS:
            user_notes:
                Required Argument.
                The list of UserNote objects.
                Type: List[UserNote]
        """
        self._user_notes = user_notes
        
    def to_json(self):
        json_representations = []
        for note in self._user_notes:
            json_representations.append(note.to_json())
        return json_representations

    @staticmethod
    def _get_notes(notes):
        if isinstance(notes, list):
            return "".join([f"<li style='margin:0 0 5px 0;'> {note} </li>" for note in notes])
        return notes

    @staticmethod
    def _get_html_cls(notification_type):
        if notification_type == UserNoteType.PARTIALLY_SUPPORTED.name:
            return "partially_supported"
        elif notification_type == UserNoteType.NOT_SUPPORTED.name:
            return "not_supported"
        return "notification"
    
    @staticmethod
    def process_notification_type(self, type_notes):
        """
        DECSRIPTION:
            Process notes of a specific notification type and combine line numbers.

        PARAMETERS:
            type_notes
                List of UserNote or NotebookUserNote objects of the same notification type.

        RETURNS:
            dict:
                A dictionary containing the combined record for the notification type.
        """

        # Start with the first note's data for this type.
        combined_rec = type_notes[0].to_json()

        # Combine start and end line numbers in the format "start-end".
        combined_lines = []
        for note in type_notes:
            if note.start_line_no and note.end_line_no:
                if note.start_line_no == note.end_line_no:
                    # Only add start line.
                    combined_lines.append(str(note.start_line_no))
                else:
                    # Add as start-end,
                    combined_lines.append(f"{note.start_line_no}-{note.end_line_no}")

        combined_rec["Start Line No"] = ", ".join(sorted(combined_lines, key=lambda x: int(x.split('-')[0]))) if combined_lines else ''
        # Use the first entry's notes for this type.
        combined_rec["Notes"] = self._get_notes(type_notes[0].user_notes)
        combined_rec["Notification Type"] = type_notes[0].note_type.name

        return combined_rec

    @staticmethod
    def _get_html_table_rows(self):
        """
        DESCRIPTION:
            Processes user notes to generate HTML table rows. It flattens nested user notes,
            groups them by object name, and combines relevant information into a structured format 
            suitable for rendering in an HTML table.

        PARAMETERS:
            None

        RETURNS:
            str:
                A string containing the HTML representation of the table rows, with each row 
                corresponding to a combined record of user notes.
        """
        # Flatten the nested list of user notes into a single list.
        if isinstance(self._user_notes, UserNote):
            flat_user_notes = [self._user_notes]
        elif isinstance(self._user_notes, list):
            flat_user_notes = []
            for item in self._user_notes:
                if isinstance(item, list):
                    flat_user_notes.extend(item)
                elif isinstance(item, UserNote):
                    flat_user_notes.append(item)

        # Group notes by object_name
        grouped_notes = defaultdict(list)
        for note in flat_user_notes:
            grouped_notes[note.object_name].append(note)

        # Create combined records
        combined_records = []

        for object_name, notes in grouped_notes.items():
            notes_by_type = defaultdict(list)
            # Start with the first note's data.
            combined_rec = notes[0].to_json()

            # Combine start and end line numbers in the format "start-end".
            combined_lines = []
            for note in notes:
                notes_by_type[note.note_type].append(note)
            
            for note_type, type_notes in notes_by_type.items():
                combined_rec = self.process_notification_type(self, type_notes)
                combined_records.append(combined_rec)

        # Sort the combined records only if "Start Line No" is not empty.
        if any(rec["Start Line No"] for rec in combined_records) and any(rec["End Line No"] for rec in combined_records):
            records = sorted(
                combined_records,
                key=lambda rec: (
                    min(int(note.split('-')[0]) for note in rec["Start Line No"].split(", ") if note),  
                    rec["Object Name"]
                )
            )
        else:
            records = combined_records

        row_template = """
        <tr>      

              <td class="{html_cls}">{sno}</td>

              <td class="{html_cls}">{line_no}</td>
              
              <td class="{html_cls}">{python_obj_name}</td>
              
              <td class="{html_cls}">{notes}</td>
              
          </tr>
        """
        result = []
        sno=1
        for rec in records:
            html_row = row_template.format(
                html_cls=self._get_html_cls(rec["Notification Type"]),
                sno = sno,
                line_no=rec["Start Line No"],  
                python_obj_name=rec["Object Name"] if rec["Object Name"]!='udfs' else 'udf',
                notes=rec["Notes"]
            )
            result.append(html_row)
            sno +=1
        return "".join(result)
    
class ScriptNotes(UserNotes):
    def __init__(self, user_notes, filepath):
        super().__init__(user_notes)
        self.filepath = filepath

    template =  """
        <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8"/>
                <title>pyspark2teradataml</title>
                <style>
                    body {{
                      font-family: Helvetica, Arial, sans-serif;
                      font-size: 12px;
                      position: relative;
                      float: left;
                      width: 100%;
                      margin:0;
                  }}
            
                  .heading {{
              font-size: 30px;
              position: relative;
              float: left;
              width: 100%;
              text-align: center;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
                  .imp_notes {{
              font-size: 20px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            .how_to_interpret {{
              font-size: 12px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            p {{
              color: black;
            }}
            
            a {{
              color: #999;
            }}
            
            
            table {{
              /* border: #E1EcF4 1px solid; */
              border: #E1EcF4 1px solid;
              border-collapse: collapse;
              margin-top: 35px;
              margin-left: 5px;
              margin-right: 5px;
              margin-bottom: 5px;
            }}
            
            tr {{
              border-bottom: #E1EcF4 1px solid;
              height:35px;
              /* padding-top: 5px;
              padding-bottom: 5px; */
            }}
            
            .orange_background {{
              color: chocolate;
            }}
            
            th {{
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:center;
              background-color:#E1EcF4; 
              color:#6A737C; 
              font-size:13px;
              border-right: #ddd 1px solid;
            }}
            
            td {{
              border-right: #E1EcF4 1px solid;
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:left;
              padding-bottom: 5px;
              padding-top: 5px;
            }}
            
            .not_supported {{
              color: red;
            }}
            
            .partially_supported {{
              color: blue;
            }}
            
            .notification {{
              color: black;
            }}
            
            </style>
              </head>
              <body>
                  <span class="heading"> pyspark2teradataml - {filename} </span>
                  <span class="imp_notes">Important Notes: </span>
                    <ul>
                  
                    <li>Refer user guide and supportability matrix for ML functions. </li>
					<li>Some functions are not supported however they are supported with manual code changes. Look at the section 'Examples' in the user guide to know more details.  </li>
					<li>ML Functions accepts multiple columns for arguments. Hence, no need to pass vectors, update the script to pass multiple columns. </li>
					<li>RDD API's are not applicable to Vantage. Make use of DataFrame API's. </li>
					<li>Columns are case sensitive in teradatamlspk and they are case insensitive in PySpark. Convert the column names to appropriate case while converting the code. </li>
                    <li>DataFrame.rdd returns same DataFrame as RDD is not applicable to Vantage. Hence use DataFrame API's and do not use RDD API's. </li>
                    <li>pyspark2teradataml does not modify the SQL statements. Users are advised to manually update the SQL statements if the corresponding SQL statement is not valid in Vantage. </li>
                    <li>teradatamlspk timezone strings don't consider Daylight Saving Time(DST). Users are advised to use teradata vantage timezone strings for DST consideration.</li>
                    <li>DataFrame.sort(), DataFrame.orderBy() </li> 
                    <ul>
                    <li>Does not propogate the changes to next API. </li> 
                    <li>To get top n elements or bottom n elements, use ranking with window aggregates and filter it. </li>
                    <li>ColumnExpressions are not supported. Only Column names are supported.</li>
                    </ul>
                  </ul>
                  <h3>Text in below table in any of below three colors. Every color has significance as explained below: </h3>
                  <ul>
                  
                    <li><span style="color: red; text-decoration: underline;">red</span>: These API's do not have functionality in teradatamlspk. User need to achieve the functionality through some other way. </li>
                    <li><span style="color: blue; text-decoration: underline;">blue </span>: These API's have functionality but there may be some difference in functionality when compared with PySpark. Notes specifies what is the exact difference so user should change it manually. </li>
                    <li><span style="color: black; text-decoration: underline;">black </span>: This is for a notification to user. <b> No action required. </b> </li>
                  </ul>
                  <div id="html_table">
                    {table}
                  </div>
              </body>
            </html>
        
        """

    def to_html(self):
        table = self._get_html_table()
        filename = os.path.basename(self.filepath)
        return self.template.format(filename=filename, table=table)
        
    def _get_html_table(self):
        html_table = """
        <table>
          <tr >

              <th>SNO</th>
              
              <th>Line No</th>
          
              <th>Object Name</th>
              
              <th>Notes</th>
          </tr>
          
          {rows}
                  
        </table>
        """
        rows = self._get_html_table_rows(self)
        return html_table.format(rows=rows)
 
class DirectoryNotes(UserNotes):

    def __init__(self, user_notes, filepath, filename):
        super().__init__(user_notes)
        self.filepath = filepath
        self.filename = filename

    template =  """
        <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8"/>
                <title>pyspark2teradataml</title>
                <style>
                    body {{
                      font-family: Helvetica, Arial, sans-serif;
                      font-size: 12px;
                      position: relative;
                      float: left;
                      width: 100%;
                      margin:0;
                  }}
            
                  .heading {{
              font-size: 30px;
              position: relative;
              float: left;
              width: 100%;
              text-align: center;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
                  .imp_notes {{
              font-size: 20px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            .how_to_interpret {{
              font-size: 12px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            p {{
              color: black;
            }}
            
            a {{
              color: #999;
            }}
            
            
            table {{
              /* border: #E1EcF4 1px solid; */
              border: #E1EcF4 1px solid;
              border-collapse: collapse;
              margin-top: 35px;
              margin-left: 5px;
              margin-right: 5px;
              margin-bottom: 5px;
            }}
            
            tr {{
              border-bottom: #E1EcF4 1px solid;
              height:35px;
              /* padding-top: 5px;
              padding-bottom: 5px; */
            }}
            
            .orange_background {{
              color: chocolate;
            }}
            
            th {{
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:center;
              background-color:#E1EcF4; 
              color:#6A737C; 
              font-size:13px;
              border-right: #ddd 1px solid;
            }}
            
            td {{
              border-right: #E1EcF4 1px solid;
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:left;
              padding-bottom: 5px;
              padding-top: 5px;
            }}
            
            .not_supported {{
              color: red;
            }}
            
            .partially_supported {{
              color: blue;
            }}
            
            .notification {{
              color: black;
            }}
            
            </style>
              </head>
              <body>
                  <span class="heading"> pyspark2teradataml - {dirname} </span>
                  <span class="imp_notes">Important Notes: </span>
                  <ul>
                  
                    <li>Refer user guide and supportability matrix for ML functions. </li>
					<li>Some functions are not supported however they are supported with manual code changes. Look at the section 'Examples' in the user guide to know more details.  </li>
					<li>ML Functions accepts multiple columns for arguments. Hence, no need to pass vectors, update the script to pass multiple columns. </li>
					<li>RDD API's are not applicable to Vantage. Make use of DataFrame API's. </li>
					<li>Columns are case sensitive in teradatamlspk and they are case insensitive in PySpark. Convert the column names to appropriate case while converting the code. </li>
                    <li>DataFrame.rdd returns same DataFrame as RDD is not applicable to Vantage. Hence use DataFrame API's and do not use RDD API's. </li>
                    <li>pyspark2teradataml does not modify the SQL statements. Users are advised to manually update the SQL statements if the corresponding SQL statement is not valid in Vantage. </li>
                    <li>DataFrame.sort(), DataFrame.orderBy() </li> 
                    <ul>
                    <li>Does not propogate the changes to next API. </li> 
                    <li>To get top n elements or bottom n elements, use ranking with window aggregates and filter it. </li>
                    <li>ColumnExpressions are not supported. Only Column names are supported.</li>
                    </ul>
                  </ul>
                  <h3>Text in below table in any of below three colors. Every color has significance as explained below: </h3>
                  <ul>
                  
                    <li><span style="color: red; text-decoration: underline;">red</span>: These API's do not have functionality in teradatamlspk. User need to achieve the functionality through some other way. </li>
                    <li><span style="color: blue; text-decoration: underline;">blue </span>: These API's have functionality but there may be some difference in functionality when compared with PySpark. Notes specifies what is the exact difference so user should change it manually. </li>
                    <li><span style="color: black; text-decoration: underline;">black </span>: This is for a notification to user. <b> No action required. </b> </li>
                  </ul>
                  <div id="html_table">
                    {table}
                  </div>
              </body>
            </html>
        
        """
     
    def to_html(self):
        table = self._get_html_table()
        dirname = os.path.basename(self.filepath)
        return self.template.format(dirname=dirname, table=table)
    
    def _get_html_table(self):
        html_table = """
        <table>
          <tr>

            <th colspan="4" style="text-align: left; background-color: #f1e7f6;">File: {filename}</th>
          </tr>

          <tr >

              <th>SNO</th>
              
              <th>Line No</th>
          
              <th>Object Name</th>
              
              <th>Notes</th>
          </tr>
          
          {rows}
                  
        </table>
        """
        rows = self._get_html_table_rows(self)
        return html_table.format(filename=self.filename, rows=rows)


class NotebookNotes(ScriptNotes):
    def __init__(self, user_notes, filepath):
        super().__init__(user_notes, filepath)
        self.filepath = filepath

    def _get_html_table(self):
        html_table = """
        <table>
          <tr >

              <th>Cell No</th>
          
              <th>Line No</th>
          
              <th>Object Name</th>
              
              <th>Notes</th>
          </tr>
          
          {rows}
                  
        </table>
        """
        rows = self._get_html_table_rows()
        return html_table.format(rows=rows)

    def extract_cell_no_key(self, cell_no):
    # Extract the non-numeric and numeric parts of the cell_no for sorting in html table.
        match = re.match(r"([^\d]*)(\d*)", str(cell_no))
        # Return a tuple of the non-numeric part and the numeric part as an integer.
        return (match.group(1), int(match.group(2) or 0))

    def _get_html_table_rows(self):
    # Flatten the nested list of user notes into a single list, handling both UserNote and list cases.
        if isinstance(self._user_notes, NotebookUserNote):
            flat_user_notes = [self._user_notes]
        elif isinstance(self._user_notes, list):
            flat_user_notes = []
            for item in self._user_notes:
                if isinstance(item, list):
                    flat_user_notes.extend(item)
                elif isinstance(item, NotebookUserNote):
                    flat_user_notes.append(item)

        # Group notes by cell_no first and then by object_name.
        grouped_cell_no = defaultdict(list)
        for note in flat_user_notes:
            grouped_cell_no[note.cell_no].append(note)

        combined_records = []
        for cell_no, cell_notes in grouped_cell_no.items():
            # Group notes by object_name and combine them.
            grouped_notes = defaultdict(list)
            for note in cell_notes:
                grouped_notes[note.object_name].append(note)

            # Create combined records.
            for object_name, object_notes in grouped_notes.items():
                notes_by_type = defaultdict(list)
                for note in object_notes:
                    notes_by_type[note.note_type].append(note)

                for note_type, type_notes in notes_by_type.items():
                    combined_rec = self.process_notification_type(self, type_notes)
                    # Add cell number for notebooks.
                    combined_rec["Cell No"] = cell_no
                    combined_records.append(combined_rec)

        # Sort the combined records only if "Start Line No" is not empty.
        if any(rec["Start Line No"] for rec in combined_records) and any(rec["End Line No"] for rec in combined_records):
            records = sorted(combined_records,
                key=lambda rec: ( self.extract_cell_no_key(rec["Cell No"]),
                    min(int(note.split('-')[0]) for note in rec["Start Line No"].split(", ") if note),
                    rec["Object Name"]
                )
            )
        else:
            records = combined_records

        row_template = """
        <tr>
              <td class="{html_cls}">{cell_no}</td>
        
              <td class="{html_cls}">{start_ln_no}</td>
              
              <td class="{html_cls}">{python_obj_name}</td>
              
              <td class="{html_cls}">{notes}</td>
              
          </tr>
        """
        result = []
        for rec in records:
            html_row = row_template.format(
                html_cls=self._get_html_cls(rec["Notification Type"]),
                cell_no=rec["Cell No"],
                start_ln_no=rec["Start Line No"],
                python_obj_name=rec["Object Name"] if rec["Object Name"]!='udfs' else 'udf',
                notes=rec["Notes"]
            )
            result.append(html_row)
        return "".join(result)

class PyCode:

    def __init__(self, code_or_ast, parse_function_body=False):
        self.__ast = code_or_ast
        self.__parse_function_body = parse_function_body
        
    def get_statements(self):
        """
        DESCRIPTION:
            Function to get all the corresponding python statements one by one.

        PARAMETERS:
            None

        RETURNS:
            generator:
                Yields AST objects from the script.
                Type: ast.AST
        """
        # If input is of code then parse it.
        if isinstance(self.__ast, str):
            self.__ast = ast.parse(self.__ast)

        for node in self._get_python_stmts(self.__ast):
            yield node  


    def _get_python_stmts(self, node):
        """
        DESCRIPTION:
            Yields Python statements from an AST node, recursively processing nested structures.

        PARAMETERS:
            node:
                Required Argument.
                The AST node to process.
                Type: ast.AST

        RETURNS:
            generator:
                Yields individual AST nodes representing Python statements.
                Type: ast.AST
        """
        # Check if the node is one of the target types and yield it.
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Expr, ast.Assign,
                             ast.AnnAssign, ast.Constant)):
            yield node

        elif isinstance(node, ast.Return):
            if node.value:  # Check if there's a return value
                yield node.value
            else:
                yield node 
        elif isinstance(node, ast.FunctionDef):
            # If the node has a body, recursively yield statements from it.
            for decorator in node.decorator_list:
                yield decorator
            yield node
            if self.__parse_function_body:
                for stmt in node.body:
                    yield from self._get_python_stmts(stmt)

        elif isinstance(node, ast.Try):
            # Yield the try node itself.
            yield node
            # Yield all statements in the try block.
            for stmt in node.body:
                yield from self._get_python_stmts(stmt)
            # Yield all handlers (except blocks)
            for handler in node.handlers:
                yield from self._get_python_stmts(handler)
            # Yield all statements in the finally block, if it exists.
            for stmt in node.finalbody:
                yield from self._get_python_stmts(stmt)

        # Some of the objects will have body. Make sure to process it too.
        # However, do not yield function body. They should be processed during
        # the call of function.
        elif hasattr(node, 'body') and (not isinstance(node, ast.FunctionDef)):
            for stmt in node.body:
                yield from self._get_python_stmts(stmt)

        if hasattr(node, 'orelse'):
            # If the node has an orelse, recursively yield statements from it.
            for stmt in node.orelse:
                yield from self._get_python_stmts(stmt)

class _ImportParser:
    """
    DESCRIPTION:
        Parses the individual import statement.
    """
    def __init__(self, ast_obj, invalid_imports):
        self.node = ast_obj
        self.invalid_imports = invalid_imports

    def get_imports(self):
        """
        DESCRIPTION:
            Parses an import statement and returns the new import statement along with any invalid imports.

        PARAMETERS:
            node:
                Required Argument.
                The AST node representing an import statement.
                Types: ast.Import, ast.ImportFrom

        RETURNS:
            tuple:
                A tuple containing three elements:
                 str: The new import statement as a string.
                 list: A list of invalid imports.
                 list: A list of spark imports.
        """
        if isinstance(self.node, ast.Import):
            new_import, invalid_imports, spark_imports = self.parse_import()

        elif isinstance(self.node, ast.ImportFrom):
            new_import, invalid_imports, spark_imports = self.parse_from_import()
            
        else:
            return None, None, None # Indicate that there are no valid imports.
            
        return new_import, invalid_imports, spark_imports

    def parse_from_import(self):
        """
        DESCRIPTION:
            Parses an AST node representing a regular 'from... import' statement.
            This method handles PySpark imports, validating PySpark imports.
            It constructs a new import statement for valid imports and collects
            information about invalid imports.

        PARAMETERS:
            node:
                Required Argument.
                An AST node representing an 'importFrom' statement.
                Types: ast.Import

        RETURNS:
            tuple: A tuple containing two elements:
                - str: A string representing the new import statement for valid imports.
                Empty string if no valid imports are found.
                - list: A list of dictionaries containing information about invalid imports.
                Each dictionary includes 'statement', 'obj.
                - list: A list of spark imports.
        """
   
        valid_imports = []
        invalid_imports = []
        spark_imports = []

        # Check if the module starts with 'pyspark'.
        if self.node.module.startswith('pyspark'):
            if self.node.names[0].name == "*":
                # Handle * imports
                current_dict = spark_objects_ 
                module_parts = self.node.module.split('.')
                for part in module_parts:
                    current_dict = current_dict.get(part, {})
                
                # Add all keys from the current_dict to spark imports.
                for key in current_dict.keys():
                    spark_imports.append(key)
                
                # Create a new import statement for * import
                new_import = f"from {self.node.module} import *"
                return new_import, [], spark_imports
            else:
                for imported_lib in self.node.names:
                    # Construct the import statement, handling aliases if present.
                    imported_stmt_ = imported_lib.name if (imported_lib.asname is None) else f"{imported_lib.name} as {imported_lib.asname}"
                    
                    # Create a dictionary with import information 
                    import_info = {
                        'statement': imported_stmt_,
                        'obj': imported_lib.name
                    }
                    # Add directly to spark_imports since it is a pyspark import.
                    spark_imports.append(imported_lib.name)
                    # Check if the import is invalid (in invalid_imports).
                    if imported_lib.name in self.invalid_imports:
                        invalid_imports.append(import_info)
                    else:
                        valid_imports.append(import_info)
        
                # Construct the new import statement if there are valid imports.
                if valid_imports:
                    new_import = f"from {self.node.module} import {', '.join([imp['statement'] for imp in valid_imports])}"
                    return new_import, invalid_imports, spark_imports
                else:
                    return "", invalid_imports, spark_imports
        else:
            return None, None, None
        
    def parse_import(self):
        """
        DESCRIPTION:
            Parses an AST node representing a regular 'import' statement.
            This method handles both PySpark and non-PySpark imports, validating
            PySpark imports and considering all non-PySpark imports as valid.
            It constructs a new import statement for valid imports and collects
            information about invalid imports.

        PARAMETERS:
            node:
                Required Argument.
                An AST node representing an 'import' statement.
                Types: ast.Import

        RETURNS:
            tuple: A tuple containing two elements:
                - str: A string representing the new import statement for valid imports.
                Empty string if no valid imports are found.
                - list: A list of dictionaries containing information about invalid imports.
                Each dictionary includes 'statement', 'obj'.
                - list: A list of spark imports.
        """
        valid_imports = []
        invalid_imports = []
        spark_imports = []
        is_valid = True
        leaf_part = None

        for name in self.node.names:
            # Split the import name into parts.
            parts = name.name.split('.')
            
            # Check if the import starts with 'pyspark'.
            if parts[0] == 'pyspark':
                leaf_part = parts[-1]
                is_valid =  leaf_part not in self.invalid_imports
                spark_imports.append(leaf_part)
            else:
                is_valid = True

            # Construct the import statement, handling aliases if present.
            imported_stmt_ = name.name if name.asname is None else f"{name.name} as {name.asname}"
            
            # Create a dictionary with import information including line numbers.
            import_info = {
                'statement': imported_stmt_,
                'obj' : leaf_part
            }

            if is_valid:
                valid_imports.append(import_info)
            else:
                invalid_imports.append(import_info)

        # If there are valid imports, construct the new import statement.
        if valid_imports:
            new_import = f"import {', '.join([imp['statement'] for imp in valid_imports])}"
            if new_import == ast.unparse(self.node):
                # If same as original import then don't need to consider the new one.
                return None, None, None
            return new_import, invalid_imports, spark_imports
        else:
            if spark_imports and invalid_imports:
                return  "", invalid_imports, spark_imports
            return None, None, None

class Script:
    def __init__(self, path):
        """
        DESCRIPTION:
            Specifies the file path for the script to be processed.

        PARAMETERS:
            path:
                Required Argument.
                Specifies the absolute or relative path for the script file.
                Type: str
        """
        self._path = path
        self.python_statements = []
        self.__code = None
        self.content = None
        self._udf_ids = set()
        self._spark_variables = {"spark"}
        self._spark_imports = set()
        self._python_functions = {}
        self.cell_no = None
        self._script_notes = []
        self.pyspark_to_tdmlspk= {            
            "pyspark": "teradatamlspk",
            "SparkSession": "TeradataSession",
            "SparkContext": "TeradataContext",
            'SparkConf': "TeradataConf",
            '.sparkContext': ".teradataContext",
            "sparkUser": "teradataUser",
            'getOrCreate()': "getOrCreate(host=getpass.getpass('Enter host: '), user=getpass.getpass('Enter user: '), password=getpass.getpass('Enter password: '))"
        }
        
        with open(self._path) as fp:
            self.content = fp.readlines()
            self.content.insert(0, "")

            # readlines already makes pointer to go end.
            fp.seek(0) 
            self.__code = PyCode(fp.read())

    def _get_name(self, arg):
        """Get the name of argument"""
        if isinstance(arg, ast.Name):
            return arg.id
        elif isinstance(arg, ast.Attribute):
            return arg.attr

    def _process_function_definition(self, func_def, cell_count=None, cell_no=None):
        """
        DESCRIPTION:
            Processes a function definition, analyzing its body for PySpark related statements
            and updating the script's content with any necessary modifications.

        PARAMETERS:
            func_def:
                Required Argument.
                The AST node representing the function definition to process.
                Type: ast.FunctionDef

            cell_count:
                Optional Argument.
                Not used in this function. Added for consistency with other functions.

            cell_no:
                Optional Argument.
                Not used in this function. Added for consistency with other functions.

        RETURNS:
            None
        """
        function_notes = set()
        # Create a new PyCode instance with the function definition.
        py_code = PyCode(func_def, parse_function_body=True)

        # Process each statement in the function body.
        for stmt in py_code.get_statements():
            statement = PythonStatement(stmt)

            imports, variables, _ = statement.process(self._spark_imports, self._spark_variables)
            # Update the sets of PySpark variables and imports.
            self._spark_variables = self._spark_variables.union(variables)
            self._spark_imports = self._spark_imports.union(imports)

            # Collect any user guide notes for this statement.
            user_guide = statement.get_user_guide()
            if user_guide:
                function_notes = function_notes.union(set(user_guide))

            # If the statement was modified, update the content of the script
            if statement.modified_statement is not None:
                start_line = statement.ast_obj.lineno
                end_line = statement.ast_obj.end_lineno

                # Get the indentation of the original line
                original_indent = self._get_indentation(self.content[start_line])

                # Apply the original indentation to the modified statement.
                indented_modified_statement = original_indent + statement.modified_statement.lstrip()

                # Replace the line(s) in self.content.
                self.content[start_line] = indented_modified_statement + '\n'
                for line in range(start_line+1, end_line+1):
                    self.content[line] = '\n'

            # Recursively process nested function calls
            self._process_potential_function_call(statement)

        # Add all collected notes to the script's notes
        self._script_notes = list(set(self._script_notes).union(function_notes))

    def _get_indentation(self, line):
        """Get indentation for the given line."""
        return line[:len(line) - len(line.lstrip())]

    def process(self, publish_user_guide=True):
        """
        DESCRIPTION:
            Processes each and every statement in the script.

        PARAMETERS:
            publish_user_guide:
                Optional Argument.
                Determines whether to publish the user guide.
                Type: bool
                Default: True

        RETURNS:
            None
        """

        # Think like this as running a python script. Below are the steps during the actual run of script:
        #   First process all the statements. This step will ensure script has no syntax errors.
        #   Then load all the functions. Once functions are loaded, then process the statements one by one.
        #   While looking at statements, identify function calls. When such function call is identified,
        #   then process the corresponding function.
        try:
            for py_statement in self.__code.get_statements():
                if isinstance(py_statement, ast.FunctionDef):
                    # Find function have decorator or not,
                    # If yes then check decorator id is 'pandas_udf'
                    # If yes then add to 'self._udf_ids'
                    for decorators in py_statement.decorator_list:
                        if isinstance(decorators, ast.Call) and \
                                isinstance(decorators.func, ast.Name) and \
                                decorators.func.id == 'pandas_udf':
                            self._udf_ids.add(py_statement.name)
                    self._python_functions[py_statement.name] = py_statement
                else:
                    self.python_statements.append(PythonStatement(py_statement))
        except SyntaxError:
            self._script_notes.append(UserNote("", "", "", "Script has Syntax errors. Unable to parse it.", UserNoteType.NOT_SUPPORTED))
            self.publish_user_guide()
            return
        # If you are here, script is good and all statements are in hand.
        for statement in self.python_statements:
            imports, variables, udf_ids = statement.process(self._spark_imports, self._spark_variables, self._udf_ids)
            # Add the returned variable to script variables so subsequent
            # statements consume the variables.
            self._spark_variables = self._spark_variables.union(variables)
            self._spark_imports = self._spark_imports.union(imports)
            self._udf_ids = self._udf_ids.union(udf_ids)
            # process function calls.
            self._process_potential_function_call(statement)

        # After processing all the functions that are called, and 
        # still if self._python_functions is not empty then call for those.
        if self._python_functions:
            remaining_functions = list(self._python_functions.items())
            for func_name, func_def in remaining_functions:
                if func_name in self._python_functions:
                    # Delete these in python functions to avoid reprocessing.
                    del self._python_functions[func_name]

                # Add all the function args in the self.spark_variables.
                for arg in func_def.args.args:
                    if isinstance(arg, ast.arg):
                        arg_name = arg.arg
                        self._spark_variables.add(arg_name)

                self._process_function_definition(func_def)

        self.publish_tdmlspk_script()

        if publish_user_guide:
            # publish user guide.
            self.publish_user_guide()

    def _process_potential_function_call(self, statement, cell_count=None):
        """
        DESCRIPTION:
            Processes a potential function call within a statement, checking if it's a defined Python function
            and analyzing its arguments for PySpark-related content.

        PARAMETERS:
            statement:
                Required Argument.
                The statement object containing the potential function call.
                Type: PythonStatement

            cell_count:
                Optional Argument.
                The cell count of the function definition.
                Type: int
                Default: None

        RETURNS:
            None
        """
        # Check if the statement contains a single function call.
        if statement._deque and len(statement._deque) == 1 and isinstance(statement._deque[0], ast.Call):
            func_call = statement._deque[0]
            func_name = self._get_name(func_call.func)
            # Check if the function is in stored functions.
            if func_name in self._python_functions:
                # Get the function definition, cell_count and cell_no.
                func_data = self._python_functions[func_name]
                func_def = func_data[0] if cell_count else func_data
                cell_count = func_data[1] if cell_count else None
                cell_no = func_data[2] if cell_count else None
                # Remove the function from _python_functions to avoid reprocessing.
                del self._python_functions[func_name]

                # Process each argument of the function call.
                for i, arg in enumerate(func_call.args):
                    arg_name = self._get_name(arg)
                    if i < len(func_def.args.args):
                        corresponding_arg = func_def.args.args[i]
                        corresponding_arg_name = corresponding_arg.arg

                        # Check if the argument is passed from Spark variables.
                        if self._is_spark_related(arg):
                            self._spark_variables.add(corresponding_arg_name)

                        # Check if the argument type annotation is spark related.
                        if hasattr(corresponding_arg, 'annotation'):
                            annotation = self._get_name(corresponding_arg.annotation)
                            if annotation in self._spark_imports or annotation in self._spark_variables:
                                self._spark_variables.add(corresponding_arg_name)

                # Process the function definition.
                self._process_function_definition(func_def, cell_count, cell_no)

    def _is_spark_related(self, node):
        """
        Recursively check if a node or its attributes are Spark-related.
        """
        if isinstance(node, ast.Name):
            return node.id in self._spark_imports or node.id in self._spark_variables
        elif isinstance(node, ast.Attribute):
            return self._is_spark_related(node.value) or node.attr in self._spark_imports or node.attr in self._spark_variables
        elif isinstance(node, ast.Call):
            return self._is_spark_related(node.func) or any(self._is_spark_related(arg) for arg in node.args)
        return False          

    def is_multiple_statements_involved(self, start_line, end_line):
        """Check if there are multiple statements involved between start_line and end_line."""
        # Extract the relevant lines from content.
        relevant_lines = self.content[start_line:end_line + 1]
    
        # Join the lines into a single string for parsing.
        combined_statement = ''.join((line.strip() for line in relevant_lines))
        try:
            parsed_ast = ast.parse(combined_statement)
        except IndentationError:
            return True
        # If length is more than 1 multiple statements are involved.
        return len(parsed_ast.body) > 1

    def publish_tdmlspk_script(self):
        """
        DESCRIPTION:
            Look at processed statements and replaces 'self.content' with the modified script.
        """
        for statement in self.python_statements:
            # Only update the self.content for those which are modified.
            if statement.modified_statement is not None:
                start_line = statement.ast_obj.lineno
                end_line = statement.ast_obj.end_lineno

                if isinstance(statement.ast_obj, (ast.Import, ast.ImportFrom)):

                    if(start_line ==  end_line):
                        if not self.is_multiple_statements_involved(start_line, end_line):
                            self.content[start_line] = statement.modified_statement + '\n'
                        
                    else:
                        # only update the start_line with the statement.modified_statement and put the next line empty.
                        self.content[start_line] = statement.modified_statement + '\n'

                        for line in range(start_line+1, end_line+1):
                            self.content[line] = '\n'
                else: 
                    # If multiple statements are involved in same line don't replace it.
                    if not self.is_multiple_statements_involved(start_line, end_line):
    
                        self.content[start_line] = statement.modified_statement + '\n'

                        for line in range(start_line+1, end_line+1):
                            self.content[line] = '\n'

        # Adding getpass for the 1st import statememt.
        for idx, line in enumerate(self.content):
            if line.startswith("import ") or line.startswith("from "):
                self.content[idx] = f"import getpass; {line}"  
                break
        
        # Updating pyspark to tdmlspk.
        for idx, line in enumerate(self.content):
            for pyspark_script, tdmlspk_script in self.pyspark_to_tdmlspk.items():
                self.content[idx] = self.content[idx].replace(pyspark_script, tdmlspk_script)
        
        new_file_path = new_file_path = self.generate_output_file_path_for_file(is_script=True)
        with open(new_file_path, 'w') as fp:
            fp.writelines(self.content)

        print("Python script '{}' converted to '{}' successfully.".format(self._path, new_file_path))

    def generate_output_file_path_for_file(self, is_script=True):
        """
        Generates the output file path for the processed script/ notebook.

        PARAMETERS:
            is_script:
                Optional Argument.
                Determines if the output file is a script or a notebook.
                Type: bool
                Default: True

        RETURNS:
            str: The full path of the output file.
        """
        dir_name = os.path.dirname(self._path)
        base_name = os.path.basename(self._path)

        # Remove the .py extension if it exists.
        file_name = os.path.splitext(base_name)[0]

        # Create a new file name with _tdmlspk suffix.
        new_file_name = f"{file_name}_tdmlspk.py" if is_script else f"{file_name}_tdmlspk.ipynb"
        return os.path.join(dir_name, new_file_name)
    
    def generate_output_file_path_for_user_guide(self):
        """
        Generates the output file path for the processed script.

        RETURNS:
            str: The full path of the output file.
        """
        dir_name = os.path.dirname(self._path)
        base_name = os.path.basename(self._path)
        
        # Remove the .py extension if it exists.
        file_name = os.path.splitext(base_name)[0]
        
        # Create a new file name with _tdmlspk suffix.
        new_file_name = f"{file_name}_tdmlspk.html"
        return os.path.join(dir_name, new_file_name)

    def publish_user_guide(self):
        """
        DESCRIPTION:
            Loop through all the statements. Collect the individual user guide for every
            statement. Sort it according to line number. Then use the template for script
            and publish the HTML report.

        Note: Incase if python script has syntax errors, then it won't have any
              individual statements. In such cases also, this function should publish the report
              stating the file has syntax errors.
        """
        html_data =  ScriptNotes(self.get_user_notes(), self._path).to_html()

        new_file_path = self.generate_output_file_path_for_user_guide()
        with open(new_file_path, 'w') as fp:
            fp.writelines(html_data)

        print("Script conversion report '{}' published successfully. ".format(new_file_path))

    def get_user_notes(self):
        """
        DESCRIPTION:
            Retrieves and combines the list of user notes from the script and individual statements.

        PARAMETERS:
            None

        RETURNS:
            list:
                A combined list of user notes from the script and all processed statements.
                Elements are a combination of:
                    - Script-level notes (self._script_notes).
                    - User guides from each processed statement.
                Type: List[UserNote]
        """
        return self._script_notes + [statement.get_user_guide() for statement in self.python_statements]


class Notebook(Script):
    def __init__(self, path):
        super().__init__(path)
        self.python_statements = {}
        with open(self._path, encoding='utf-8') as fp:
            self.notebook = nbformat.read(fp, nbformat.NO_CONVERT)

    def process(self):
        empty_cell = 0
        cell_count = 1
        # Process all the statements in the cells of a notebook. To ensure each cell does not have syntax errors.
        # Store the statements in a dictionary with cell count(in order) as key and list of statements as value.
        # Then load all the functions. Once functions are loaded, then process the statements one by one.
        # While looking at statements, identify function calls. When such function call is identified,
        # then process the corresponding function.

        # cell_no is the cell number which is displayed in the notebook i.e Execution Count.
        # cell_count is the cell number in order.
        for cell in self.notebook['cells']:
            cell_no = cell['execution_count'] if cell['cell_type'] == 'code' else 0
            if cell_no is None:
                # If execution count is None add 'Empty Cell <No of empyty cell>' i.e. 'Empty Cell 1'
                # to track cell with no execution count in the HTML report.
                empty_cell = empty_cell+1
                cell_no = 'Empty Cell {}'.format(empty_cell)
            self.__code = PyCode(cell['source'])
            try:
                self.python_statements[cell_count] = []
                if cell['cell_type'] == 'code':
                    for py_statement in self.__code.get_statements():
                        if isinstance(py_statement, ast.FunctionDef):
                            self._python_functions[py_statement.name] = (py_statement, cell_count, cell_no)
                        else:
                            # Create a PythonStatement object for each statement
                            python_statement = PythonStatement(py_statement, cell_no)
                            # Append the PythonStatement object to the list of statements for the cell
                            self.python_statements[cell_count].append(python_statement)
                cell_count = cell_count + 1
            except SyntaxError:
                self._script_notes.append(NotebookUserNote("", "", "", "", "Notebook has Syntax errors. Unable to parse it.", UserNoteType.NOT_SUPPORTED))
                self.publish_user_guide()
                return

        for cell_count, cell_statements in self.python_statements.items():
            for statement in cell_statements:
                imports, variables, _ = statement.process(self._spark_imports, self._spark_variables)
                # Add the returned variable to notebook variables so subsequent
                # statements consume the variables.
                self._spark_variables = self._spark_variables.union(variables)
                self._spark_imports = self._spark_imports.union(imports)

                self._process_potential_function_call(statement, cell_count)

        # After processing all the functions that are called, and 
        # still if self._python_functions is not empty then call for those.
        if self._python_functions:
            remaining_functions = list(self._python_functions.items())
            for func_name, func_data in remaining_functions:
                # Get the function definition, cell_count and cell_no.
                func_def = func_data[0]
                cell_count = func_data[1]
                cell_no = func_data[2]
                if func_name in self._python_functions:
                    # Delete these in python functions to avoid reprocessing.
                    del self._python_functions[func_name]

                # Add all the function args in the self.spark_variables.
                for arg in func_data[0].args.args:
                    if isinstance(arg, ast.arg):
                        arg_name = arg.arg
                        self._spark_variables.add(arg_name)
                # Process the function definition.
                self._process_function_definition(func_def, cell_count, cell_no)

        self.publish_tdmlspk_notebook()
        self.publish_user_guide()

    def _process_function_definition(self, func_def, cell_count, cell_no):
        """
        DESCRIPTION:
            Processes a function definition, analyzing its body for PySpark related statements
            and updating the script's content with any necessary modifications.

        PARAMETERS:
            func_def:
                Required Argument.
                The AST node representing the function definition to process.
                Type: ast.FunctionDef

            cell_count:
                Required Argument.
                The cell number in order. Required to fetch cell content.
                Type: int

            cell_no:
                Required Argument.
                The cell number displayed in the notebook. Required for user guide.
                Type: int, str

        RETURNS:
            None
        """

        function_notes = set()
        # Create a new PyCode instance with the function definition.
        py_code = PyCode(func_def, parse_function_body=True)
        # Process each statement in the function body.
        for stmt in py_code.get_statements():
            # Get the content of the cell.
            self.content = self.notebook['cells'][cell_count-1]['source'].splitlines()
            self.content.insert(0, "")

            statement = PythonStatement(stmt, cell_no)
            # print(ast.unparse(statement.ast_obj))
            imports, variables,_ = statement.process(self._spark_imports, self._spark_variables)
            # Update the sets of PySpark variables and imports.
            self._spark_variables = self._spark_variables.union(variables)
            self._spark_imports = self._spark_imports.union(imports)

            # Collect any user guide notes for this statement.
            user_guide = statement.get_user_guide()
            if user_guide:
                function_notes = function_notes.union(set(user_guide))
            # If the statement was modified, update the content of the script
            if statement.modified_statement is not None:
                start_line = statement.ast_obj.lineno
                end_line = statement.ast_obj.end_lineno
                # Get the indentation of the original line
                original_indent = self._get_indentation(self.content[start_line])
                # Apply the original indentation to the modified statement.
                indented_modified_statement = original_indent + statement.modified_statement.lstrip()
                # Replace the line(s) in self.content.
                self.content[start_line] = indented_modified_statement
                for line in range(start_line+1, end_line+1):
                    self.content[line] = '\n'
            
            # Set the modified content back to the cell.
            self.content.pop(0)
            self.notebook['cells'][cell_count-1]['source'] = '\n'.join(self.content)
            # Recursively process nested function calls
            self._process_potential_function_call(statement, cell_count)
        
        # Add all collected notes to the notebook's notes
        self._script_notes = list(set(self._script_notes).union(function_notes))

    def publish_tdmlspk_notebook(self):
        """
        DESCRIPTION:
            Look at processed statements and replaces 'self.content' with the modified script.
        """
        getpass_added = False
        for cell_data, (cell_count, cell_statements) in zip(self.notebook['cells'], self.python_statements.items()):
            if cell_data['cell_type'] == 'code':
                # Remove output cell
                cell_data['outputs'] = []
                # Split the cell code string into list based on line breaks
                self.content = cell_data['source'].splitlines() 
                self.content.insert(0, "") 
                for statement in cell_statements:
                    # Only update the self.content for those which are modified.
                    if statement.modified_statement is not None:
                        start_line = statement.ast_obj.lineno
                        end_line = statement.ast_obj.end_lineno

                        if isinstance(statement.ast_obj, (ast.Import, ast.ImportFrom)):
                            if(start_line ==  end_line):
                                if not self.is_multiple_statements_involved(start_line, end_line):
                                    self.content[start_line] = statement.modified_statement
                            else:
                                # only update the start_line with the statement.modified_statement and put the next line empty.
                                self.content[start_line] = statement.modified_statement
                                for line in range(start_line+1, end_line+1):
                                    self.content[line] = '\n'
                        else:
                            # If multiple statements are involved in same line don't replace it.
                            if not self.is_multiple_statements_involved(start_line, end_line):
                                self.content[start_line] = statement.modified_statement
                                for line in range(start_line+1, end_line+1):
                                    self.content[line] = '\n'

                self.content.pop(0)

                for idx, line in enumerate(self.content):
                    # Adding getpass for the 1st import statememt.
                    if not getpass_added:
                        if line.startswith("import ") or line.startswith("from "):
                            getpass_added = True
                            self.content[idx] = f"import getpass; {line}"
                    for pyspark_script, tdmlspk_script in self.pyspark_to_tdmlspk.items():
                        self.content[idx] = self.content[idx].replace(pyspark_script, tdmlspk_script)

                cell_data['source'] = '\n'.join(self.content)

        new_file_path = new_file_path = self.generate_output_file_path_for_file(is_script=False)
        with open(new_file_path, 'w', encoding='utf-8') as fp:
                nbformat.write(self.notebook, fp, version=nbformat.NO_CONVERT)

        print("Python Notebook '{}' converted to '{}' successfully.".format(self._path, new_file_path))

    def publish_user_guide(self):
        """
        DESCRIPTION:
            Loop through all the statements. Collect the individual user guide for every
            statement. Sort it according to line number. Then use the template for script
            and publish the HTML report.

        Note: Incase if Notebook script has syntax errors, then it won't have any
              individual statements. In such cases also, this function should publish the report
              stating the file has syntax errors.
        """
        html_data =  NotebookNotes(self.get_user_notes(), self._path).to_html()

        new_file_path = self.generate_output_file_path_for_user_guide()
        with open(new_file_path, 'w') as fp:
            fp.writelines(html_data)

        print("Notebook conversion report '{}' published successfully. ".format(new_file_path))

    def get_user_notes(self):
        """
        DESCRIPTION:
            Retrieves and combines the list of user notes from the notebook and individual statements.
        PARAMETERS:
            None
        RETURNS:
            list:
                A combined list of user notes from the notebook and all processed statements.
                Elements are a combination of:
                    - Script-level notes (self._script_notes).
                    - User guides from each processed statement.
                Type: List[NotebookUserNote]
        """

        for cell, cell_statements in self.python_statements.items():
            for statement in cell_statements:
                self._script_notes.append(statement.get_user_guide())
        return self._script_notes

class Directory(Script):
    def __init__(self, path):
        self._path = path
        self._user_notes = []
        self.script_objects = []

    def __get_files(self):
        """
        DESCRIPTION:
            Internal function that recursively traverses the directory structure
            starting from self._path and yields the absolute path for each Python
            file (.py) encountered.

        PARAMETERS:
            None

        RETURNS:
                Yields absolute paths of Python files.
                Type: str
        """
        # Absolute path of each Python file found in the directory and its subdirectories.
        for root, dirs, files in os.walk(self._path):
            for file in files:
                if file.endswith('.py'):
                    yield os.path.join(root, file)

    def process(self):

        for file_ in self.__get_files():
            if file_[-2:] == "py":
                script = Script(file_)

                # Process the script.
                script.process(publish_user_guide=False)
                # collect the script objects.
                self.script_objects.append(script)

        # Publishing user guide for all the script objects.
        self.publish_user_guide()

    def publish_user_guide(self):
        """
        DESCRIPTION:
            Generates and publishes a HTML user guide for all processed scripts
            in the directory. It combines user notes from all scripts into a single HTML report,
            maintaining the structure of the first script's HTML and appending rows for
            subsequent scripts.
        """
        html_data = ""
        # Iterate through each script object.
        for sc in self.script_objects:
            filename = sc._path
            _user_notes = sc.get_user_notes()

            # Check if _user_notes is empty
            if not any(_user_notes):
                continue  # Skip to the next script if there are no user notes

            # Create a DirectoryNotes object for the current script.
            directory_notes = DirectoryNotes(_user_notes, self._path, filename)
        
            if html_data == "":
                # If it's the first script, get the full HTML including headers.
                html_data = directory_notes.to_html()
                # Remove the existing table div.
                table_div_start = html_data.find('<div id="html_table">')
                # Remove the existing table div and everything after it.
                html_data = html_data[:table_div_start]

            # Append the HTML table for the current script to the existing HTML data.
            html_data +=  directory_notes._get_html_table()

        new_file_path = self.generate_output_file_path_for_user_guide()
        with open(new_file_path, 'w') as fp:
            fp.writelines(html_data)

        print("Script conversion report '{}' published successfully. ".format(new_file_path))

def _get_json(file_path):
    """ Gets the json from a file. """
    with open(file_path, encoding='utf-8') as fp:
        return json.load(fp)

class PythonStatement:

    tdmlspk_notes = None

    def __init__(self, ast_obj, cell_no=None):

        self.ast_obj = ast_obj
        self.cell_no = cell_no
        self.start_line = ast_obj.lineno
        self.end_line = ast_obj.end_lineno
        self.is_spark_component_involved = False
        self.modified_statement = None

        # Store instances of User notes. Key should be the name of the pyspark
        # API. Value should be user notes. Example: {'Vectors': <UserNote Object>}
        self._user_notes = {}
        self.__udf_ids = set()
        self.__spark_variables = set()
        self.__spark_imports = set()
        self._current_targets = set()

        # Stores the individual elements in the statement. All the actions on
        # all types of statements except imports, be it generating user notes
        # or translating statement is done on stack.
        self._deque = deque()
        self._ml_function_args_string = '"<Specify list of column names>"'

        # populate notes.
        if PythonStatement.tdmlspk_notes is None:
            PythonStatement.tdmlspk_notes = _get_json(os.path.join(os.path.dirname(__file__), "user_guide.json"))

    def _process_setFeaturesCol_inputCols(self, actual_statement):
        # Initialize variables for tracking modifications
        modified_statement = actual_statement

        # Process function calls that set feature or input columns.
        for function in ["setFeaturesCol", "setInputCol", "setInputCols"]:
            # Regex pattern to match function calls with string or list arguments.
            # Regex pattern explanation:
            # \b({function}\s*\()  : Match the function name at a word boundary, followed by optional whitespace and an opening parenthesis
            # (                    : Start capturing group for the argument
            #  [\'"]([^\'"]*)[\'"] : Match a string argument (either single or double quotes)
            #  |                   : OR
            #  \[[^\]]*\]          : Match a list argument (anything inside square brackets)
            # )                    : End capturing group for the argument
            # (\))                 : Match the closing parenthesis
            #
            # Examples:
            #   setFeaturesCol("column_name")
            #   setInputCols(["col1", "col2"])
            pattern = rf'\b({function}\s*\()([\'"]([^\'"]*)[\'"]|\[[^\]]*\])(\))'
            matches = list(re.finditer(pattern, modified_statement))

            # Process matches in reverse order to avoid index issues when replacing.
            # We process in reverse because replacing text can change the indices of subsequent matches.
            for match in reversed(matches):
                # match.group(0): The entire matched string
                # match.group(1): The function name with opening parenthesis
                # match.group(2): The argument (either a string or a list)
                # match.group(3): The content of the string argument (if it's a string)
                # match.group(4): The closing parenthesis
                arg = match.group(2)
                if arg.startswith('"') or arg.startswith("'"):  # Check if arg is a string

                    # Replace the argument with the target string
                    # Example: If we match setFeaturesCol("column_name"),
                    # arg would be "column_name" (including the quotes)
                    replacement = f'{match.group(1)}{self._ml_function_args_string}{match.group(4)}'
                    modified_statement = modified_statement[:match.start()] + replacement + modified_statement[match.end():]
                    self.modified_statement = modified_statement
                    # Add a user note.
                    self._user_notes[function] = UserNote(self.start_line, self.end_line, function,
                        "Replace following string `Specify list of column names` with list of column names manually",
                        UserNoteType.PARTIALLY_SUPPORTED)

        # Process keyword arguments
        for keyword in ["inputCol", "inputCols", "featuresCol"]:
            # Regex pattern to match keyword arguments with string values, variable names, or lists
            # Regex pattern explanation:
            # \b({keyword}\s*=\s*)  : Match the keyword at a word boundary, followed by '=' and optional whitespace
            # (                     : Start capturing group for the entire value
            #   ([\'"]([^\'"]*)[\'"]): Match a string value (quoted content)
            #   |(\w+)              : OR match a variable name (word characters)
            #   |\[.*?\]            : OR match a list (anything between square brackets)
            # ) 
            pattern = rf'\b({keyword}\s*=\s*)(([\'"]([^\'"]*)[\'"])|(\w+)|\[.*?\])'
            
            # Find all matches of the pattern in the modified statement.
            matches = list(re.finditer(pattern, modified_statement))
            # Process matches in reverse order to avoid offsetting issues when replacing.
            for match in reversed(matches):
                full_match = match.group(0)   # The entire matched string
                keyword_part = match.group(1) # The keyword and '=' part
                value_part = match.group(2)   # The value part (string, variable, or list)
                
                # Check if the value is a string or a variable name (not a list).
                if (value_part.startswith('"') or value_part.startswith("'")) or value_part.isidentifier():
                    # Replace the matched part with the keyword and the new string.
                    replacement = f'{keyword_part}{self._ml_function_args_string}'
                    modified_statement = modified_statement[:match.start()] + replacement + modified_statement[match.end():]
                    self.modified_statement = modified_statement

                    # Add a user note.
                    if self.cell_no:
                        self._user_notes[keyword] = NotebookUserNote(self.cell_no, self.start_line, self.end_line, keyword,
                            "Replace following string `Specify list of column names` with list of column names manually",
                            UserNoteType.PARTIALLY_SUPPORTED)
                    else:
                        self._user_notes[keyword] = UserNote(self.start_line, self.end_line, keyword,
                            "Replace following string `Specify list of column names` with list of column names manually",
                            UserNoteType.PARTIALLY_SUPPORTED)

    def process(self, pyspark_imports, pyspark_variables, udf_ids=None):
        """
        DESCRIPTION:
            Processes a single statement, storing individual components if required in this object.

        PARAMETERS:
            pyspark_imports:
                Required Argument.
                Import statements specific to Spark.
                Should be provided by the Script/Notebook.
                Type: List[str]

            pyspark_variables:
                Required Argument.
                Variables which refer to Spark objects.
                Should be provided by the Script/Notebook.
                Type: List[str]

            udf_ids:
                Optional Argument.
                Function names which contains either 'lambda' or 'pandas_udf' functions.
                Type: set()

        RETURNS:
            list:
                Names of Spark variables, Spark imports, lambda functions.
                Type: List[str], set()
        """
        if isinstance(self.ast_obj, (ast.Import, ast.ImportFrom)):
            self.__process_import(self.ast_obj)
        else:
            # Parse the statement. Once statement is parsed, 'self._deque' will have
            # details of statement.
            self.__parse_statement(self.ast_obj)

            # Check if stack is populated. It can be a Name or Call object.
            # If something else, do not parse.
            if self._deque:
                variable_name = self._get_variable_name(self._deque[0])

                # If stack is populated and if variable is a spark variable, then process further.
                if variable_name and (variable_name in pyspark_imports or variable_name in pyspark_variables):
                    # Consider the whole stack as spark statements.
                    self.is_spark_component_involved = True
                    if self._current_targets:
                        self.__spark_variables = self.__spark_variables.union(self._current_targets)
                    # Handle combined attributes like read.csv, read.parquet.
                    self.process_combined_attributes()

                    for obj in self._deque:
                        keyword = self._get_variable_name(obj)

                        # If it is a call then process the arguments.
                        if isinstance(obj, ast.Call):
                            self._process_function_args(obj, pyspark_imports, pyspark_variables)

                        if keyword in ('udf', 'register'):
                            self._check_udf_register_functions(keyword, udf_ids, obj)
                            stmt = ast.unparse(self.ast_obj)
                            continue
                        self._process_keywords_call_args(obj, keyword)

                else:
                    # Only process the arguments dont check for the callable obj name.
                    for obj in self._deque:
                        # If it is a call then process the arguments.
                        if isinstance(obj, ast.Call):
                            self._process_function_args(obj, pyspark_imports, pyspark_variables)

        actual_statement = ast.unparse(self.ast_obj)

        if self.is_spark_component_involved:
            # Updation of setFeaturesCol and inputCols.
            self._process_setFeaturesCol_inputCols(actual_statement)

        return self.__spark_imports, self.__spark_variables, self.__udf_ids

    def _check_udf_register_functions(self, keyword, udf_ids, ast_obj):
        """
        DESCRIPTION:
            Updates html file if 'udf' or 'register' contains either lambda or pandas_udf function

        PARAMETERS:
            keyword:
                Required Argument.
                Specifies either 'udf' or 'register'.
                Type: str

            udf_ids:
                Required Argument.
                Function names which contains either 'lambda' or 'pandas_udf' functions.
                Type: set()

            ast_obj:
                Required Argument.
                ast object which is related to either 'udf' or 'register'.
                Type: ast object

        RETURNS:
            None
        """
        # Check if function is udf and it contains lambda function add to user notes
        stmt = ast.unparse(self.ast_obj)
        if keyword == 'udf' and 'register' not in stmt:
            flag = True
            if hasattr(ast_obj, 'keywords') and len(ast_obj.keywords) > 0:
                for keyword_arg in ast_obj.keywords:
                    if hasattr(keyword_arg, 'arg') and hasattr(keyword_arg, 'value') and \
                            keyword_arg.arg == 'f' and \
                            (isinstance(keyword_arg.value, ast.Lambda) or
                             (isinstance(keyword_arg.value, ast.Name) and udf_ids is not None and keyword_arg.value.id in udf_ids)):
                        flag = False
                        notes_ = "Lambda functions are not supported yet."
                        if self.cell_no:
                            self._user_notes[keyword] = NotebookUserNote(self.cell_no, self.start_line, self.end_line,
                                                                         keyword, notes_, UserNoteType.PARTIALLY_SUPPORTED)
                        else:
                            self._user_notes[keyword] = UserNote(self.start_line, self.end_line, keyword, notes_,
                                                                 UserNoteType.PARTIALLY_SUPPORTED)

            if flag and hasattr(ast_obj, 'args') and isinstance(ast_obj.args, list) and len(ast_obj.args) > 0:
                if isinstance(ast_obj.args[0], ast.Lambda) or \
                        (isinstance(ast_obj.args[0], ast.Name) and udf_ids is not None and ast_obj.args[0].id in udf_ids):
                    flag = False
                    notes_ = "Lambda functions are not supported yet."
                    if self.cell_no:
                        self._user_notes[keyword] = NotebookUserNote(self.cell_no, self.start_line, self.end_line,
                                                                     keyword, notes_, UserNoteType.PARTIALLY_SUPPORTED)
                    else:
                        self._user_notes[keyword] = UserNote(self.start_line, self.end_line, keyword, notes_,
                                                             UserNoteType.PARTIALLY_SUPPORTED)

            if flag:
                notes_ = "Columns passed to the UDF should be present in the corresponding DataFrame."
                self._user_notes['udfs'] = UserNote(self.start_line, self.end_line, 'udfs', notes_,
                                                      UserNoteType.PARTIALLY_SUPPORTED)
                if self.cell_no:
                    self._user_notes['udfs'] = NotebookUserNote(self.cell_no, self.start_line, self.end_line,
                                                                 'udfs', notes_, UserNoteType.PARTIALLY_SUPPORTED)
                else:
                    self._user_notes['udfs'] = UserNote(self.start_line, self.end_line, 'udfs', notes_,
                                                         UserNoteType.PARTIALLY_SUPPORTED)

        # Check if function is register and it contains lambda function or pandas_udf add to user notes
        if keyword == 'register':
            if hasattr(ast_obj, 'keywords') and len(ast_obj.keywords) > 0:
                for keyword_arg in ast_obj.keywords:
                    if hasattr(keyword_arg, 'arg') and hasattr(keyword_arg, 'value') and \
                            keyword_arg.arg == 'f' and \
                            (isinstance(keyword_arg.value, ast.Lambda) or
                             (isinstance(keyword_arg.value, ast.Name) and udf_ids is not None and keyword_arg.value.id in udf_ids)):
                        self._process_user_notes(keyword)
            elif hasattr(ast_obj, 'args') and isinstance(ast_obj.args, list) and len(ast_obj.args) > 1:
                if isinstance(ast_obj.args[1], ast.Lambda) or \
                        (isinstance(ast_obj.args[1], ast.Name) and udf_ids is not None and ast_obj.args[1].id in udf_ids):
                    self._process_user_notes(keyword)
        return self.__spark_imports, self.__spark_variables

    def _process_keywords_call_args(self, obj, keyword):
        """
        DESCRIPTION:
            Processes specific PySpark keywords and their associated function calls.
            It handles different logic for 'get', 'cast', 'agg', 'like' and 'ilike' keywords,
            analyzing their arguments and generating appropriate user notes based on
            the specific conditions for each keyword.

        PARAMETERS:
            obj:
                Required Argument.
                The AST node representing the function call or attribute being processed.
                Type: ast.Call or ast.Attribute

            keyword:
                Required Argument.
                The specific keyword being processed (for 'get', 'cast', 'agg', 'like', 'ilike').
                Type: str

        RETURNS:
            None
        """

        # Check for keyword arguments.
        keyword_args = {}
        if hasattr(obj, 'keywords'):
            keyword_args = {kwarg.arg: kwarg.value for kwarg in obj.keywords}

        if keyword == 'get':
            stmt = ast.unparse(self.ast_obj)
            if "conf.get"  not in stmt:
                self._process_user_notes(keyword)

        elif keyword == 'cast':
            # Check if the argument is a function call and its name.
            if len(obj.args) > 0 and isinstance(obj.args[0], ast.Call):
                arg = obj.args[0].func.id
                if arg in ['BooleanType', 'BinaryType', 'ArrayType', 'StructType',
                            'MapType', 'TimestampType', 'TimestampNTZType']:
                    self._process_user_notes(keyword)

            # Check keyword arguments for special types.
            for kwarg_name, kwarg_value in keyword_args.items():
                if isinstance(kwarg_value, ast.Call):
                    arg = kwarg_value.func.id
                    if arg in ['BooleanType', 'BinaryType', 'ArrayType', 'StructType',
                                'MapType', 'TimestampType', 'TimestampNTZType']:
                        self._process_user_notes(keyword)

        elif keyword == 'agg':
            # Get all argument names from the agg function.
            args = self._get_list_of_args(obj)

            # Lambda function to check if countDistinct or count_distinct has more than one argument.
            check_count_distinct_args = lambda arg: arg in ['countDistinct', 'count_distinct'] \
                and len(arg.args) > 1

            # Check positional arguments.
            if any(check_count_distinct_args(arg) for arg in obj.args):
                self._process_user_notes(keyword)

            # Check keyword arguments.
            elif any(check_count_distinct_args(value) for value in keyword_args.values()):
                self._process_user_notes(keyword)

        elif keyword in ['like', 'ilike']:
            stmt = ast.unparse(self.ast_obj)
            if '.like' not in stmt and '.ilike' not in stmt:
                args = self._get_list_of_args(obj)

                # second argument is not a ast.Name.
                second_arg_not_name = len(args) > 1 and not isinstance(obj.args[1], ast.Name)
                # Check if a third argument is present or not.
                third_arg_present = len(args) > 2

                # Call process_user_notes only if conditions are met.
                if second_arg_not_name or third_arg_present:
                    self._process_user_notes(keyword)

                # Also check keyword arguments for like conditions.
                for kwarg_value in keyword_args.values():
                    if not isinstance(kwarg_value, ast.Name):
                        self._process_user_notes(keyword)
        else:
            self._process_user_notes(keyword)

    def _get_list_of_args(self, obj):
        """Returns a list of argument names from the agg function"""
        args = []
        if isinstance(obj, ast.Call):
            for arg in obj.args:
                if isinstance(arg, ast.Call):
                    if isinstance(arg.func, ast.Name):
                        args.append(arg.func.id)
                    elif isinstance(arg.func, ast.Attribute):
                        args.append(self._get_list_of_args(arg.func))
                elif isinstance(arg, ast.Name):
                    args.append(arg.id)
                elif isinstance(arg, ast.Attribute):
                    args.append(arg.attr)

        return args

    def _process_function_args(self, obj, pyspark_imports, pyspark_variables):
        """
        DESCRIPTION:
            Processes the arguments of a function call, including both positional and keyword arguments.
            It analyzes each argument for PySpark-related content and collects user notes.

        PARAMETERS:
            obj:
                Required Argument.
                The AST node representing the function call.
                Type: ast.Call

            pyspark_imports:
                Required Argument.
                A set of PySpark imports currently known in the script.
                Type: set

            pyspark_variables:
                Required Argument.
                A set of variables currently identified as PySpark-related.
                Type: set

        RETURNS:
            None
        """
        # Process arguments if the object is a function call
        for arg in obj.args:
            arg_statement = PythonStatement(arg, self.cell_no)
            arg_imports, arg_variables, _ = arg_statement.process(pyspark_imports, pyspark_variables)
            for key, note in arg_statement._user_notes.items():
                self._user_notes[key] = note

        # Process keyword arguments
        for keyword in obj.keywords:
            keyword_statement = PythonStatement(keyword.value, self.cell_no)
            keyword_imports, keyword_variables, _ = keyword_statement.process(pyspark_imports, pyspark_variables)
            for key, note in keyword_statement._user_notes.items():
                self._user_notes[key] = note

    def process_combined_attributes(self):
        """
        DESCRIPTION:
            Processes the stack to identify and handle combined attributes,
            adding appropriate user notes.

        RETURNS:
            None
        """
        for i, obj in enumerate(self._deque):
            current_name = self._get_variable_name(obj)
            self._update_readwrite_statements(current_name)
            if current_name in combined_attributes:
                unparsed_str = ast.unparse(self.ast_obj)
                # Check the next item in the stack for a matching attribute
                for attribute in combined_attributes[current_name]:
                    if attribute in unparsed_str:
                        combined_attr = f"{current_name}.{attribute}"
                        self._process_user_notes(combined_attr)

    def _update_readwrite_statements(self, name):
        """
        DESCRIPTION:
            Add the options method to read, write and writeTo attributes,
            which user can refer or use.

        PARAMETERS:
            name:
                Required Argument.
                Specifies whether it is 'read', 'write' or 'writeTo'.
                Type: str

        RETURNS:
            None.
            Note:
                Update the script based on 'name' arg.

        EXAMPLES:
            >>> script = pyspark2teradataml("pyspark_session.read.csv('admissions_train.csv').show()")
            >>> self._update_readwrite_statements('read')
            teradatamlspk_session.read.options(authorization = {"Access_ID": "<Specify id(Required Argument)>", "Access_Key": "Specify key(Required Argument)"}).csv('admissions_train.csv').show()
        """
        if name == "read":
            stmt = ast.unparse(self.ast_obj)
            idx = stmt.index('read') + len('read')
            # read support 3 formats json, csv and parquet.
            if 'json' in stmt or 'csv' in stmt or 'parquet' in stmt:
                new_stmt = "".join([stmt[:idx],
                                    '.options(authorization = {"Access_ID": "<Specify id(Required Argument)>", "Access_Key": "Specify key(Required Argument)"})',
                                    stmt[idx:]])
                self.modified_statement = new_stmt
        elif name == "write":
            stmt = ast.unparse(self.ast_obj)
            idx = stmt.index('write') + len('write')
            # write supports 2 formats csv and parquet on cloud platform and
            # csv, orc, json and parquet on local system.
            if 'csv' in stmt or 'parquet' in stmt:
                new_stmt = "".join([stmt[:idx],'.options(authorization = {"Access_ID": "<Specify id(Required Argument)>", "Access_Key": "Specify key(Required Argument)"})',
                                    stmt[idx:]])
                self.modified_statement = new_stmt
        elif name == "writeTo":
            stmt = ast.unparse(self.ast_obj)
            idx = stmt.index('writeTo') + len('writeTo')
            # When user uses 'partitionedBy' primary_index is only option Supported and Required.
            if "partitionedBy" in stmt:
                new_stmt = "".join([stmt[:idx],
                                    '.options(primary_index="column name or tuple of column names(Required Argument)")',
                                    stmt[idx:]])
                self.modified_statement = new_stmt

    @staticmethod
    def _get_variable_name(ast_obj):
        """Get the name from ast_obj"""
        if isinstance(ast_obj, ast.Name):
            return ast_obj.id
        elif isinstance(ast_obj, ast.Call):
            if isinstance(ast_obj.func, ast.Attribute):
                return ast_obj.func.attr
            return ast_obj.func.id
        elif isinstance(ast_obj, ast.Attribute):
            return ast_obj.attr
        return 

    def _process_user_notes(self, keyword):
        """
        DESCRIPTION:
            Creates user notes.

        PARAMETERS:
            keyword:
                Required Argument.
                To check and add the corresponding UserNote a keyword.
            
        RETURNS:
            None.
        """

        not_supported = self.tdmlspk_notes.get("not_supported")
        partially_supported = self.tdmlspk_notes.get("partially_supported")
        notifications = self.tdmlspk_notes.get("notification")
        # Check and add it to corresponding NoteType.
        if keyword in not_supported:
            notes_ = not_supported[keyword]
            notes_type = UserNoteType.NOT_SUPPORTED
        elif keyword in partially_supported:
            notes_ = partially_supported[keyword]
            notes_type = UserNoteType.PARTIALLY_SUPPORTED
        elif keyword in notifications:
            notes_ = notifications[keyword]
            notes_type = UserNoteType.NO_ACTION
        else:
            notes_ = None
            notes_type = None

        # Populate the notes here.
        if notes_:
            if self.cell_no:
                self._user_notes[keyword] = NotebookUserNote(self.cell_no, self.start_line, self.end_line, keyword, notes_, notes_type)
            else:
                self._user_notes[keyword] = UserNote(self.start_line, self.end_line, keyword, notes_, notes_type)

    def __parse_statement(self, ast_obj):
        """
        DESIPTION:
            Recursively parses an AST node and stores in self.stack.

        PARAMETERS:
            ast_obj:
                Required Argument.
                The AST node to be parsed.
                Types: ast.AST
            
        RETURNS:
            None.
        """
        # If it is an expression, simply pass the value to it.
        # Do not consider anything else.
        if isinstance(ast_obj, ast.Expr):
            # Expression statement .
            # Example: print("Hello")
            self.__parse_statement(ast_obj.value)

        elif isinstance(ast_obj, (ast.Name, ast.Constant)):
            # A variable name and  constants.
            self._deque.appendleft(ast_obj)

        elif isinstance(ast_obj, (ast.Subscript)):
            # Subscript: An indexing or slicing operation.
            # Example: list[0], dict['key']
            self._deque.appendleft(ast_obj)
            self.__parse_statement(ast_obj.value)

        elif isinstance(ast_obj, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            # Assign: A regular assignment (x = y)
            # AnnAssign: An annotated assignment (x: int = 5)
            # AugAssign: An augmented assignment (x += 1)
            target_names = set()
            if isinstance(ast_obj, ast.Assign):
                # Add all lambda functions encountered to self.__udf_ids
                if hasattr(ast_obj, 'value') and \
                        isinstance(ast_obj.targets, list) and \
                        isinstance(ast_obj.value, ast.Lambda) and \
                        len(ast_obj.targets)>0 and \
                        isinstance(ast_obj.targets[0], ast.Name):
                    self.__udf_ids.add(ast_obj.targets[0].id)
                target_names = {target.id for target in ast_obj.targets if isinstance(target, ast.Name)}
            elif isinstance(ast_obj, ast.AnnAssign):
                # Add all lambda functions encountered to self.__udf_ids
                if hasattr(ast_obj, 'value') and \
                        isinstance(ast_obj.value, ast.Lambda) and \
                        isinstance(ast_obj.target, ast.Name):
                    self.__udf_ids.add(ast_obj.target.id)
                if isinstance(ast_obj.target, ast.Name):
                    target_names = {ast_obj.target.id}
            elif isinstance(ast_obj, ast.AugAssign):
                if isinstance(ast_obj.target, ast.Name):
                    target_names = {ast_obj.target.id}
            
            self._current_targets = target_names
            self.__parse_statement(ast_obj.value)

        elif isinstance(ast_obj, (ast.Tuple, ast.List)):
            # Tuple or List: A tuple or list literal.
            for element in ast_obj.elts:
                self._deque.appendleft(element)
                self.__parse_statement(element)

        elif isinstance(ast_obj, ast.Call):
            # A function call
            # If it is a call object, it will have a func. If func is Name, then store it as it is.
            if isinstance(ast_obj.func, ast.Name):
                self._deque.appendleft(ast_obj)
            elif isinstance(ast_obj.func, ast.Attribute):
                # Construct Call object.
                call_obj = ast.Call(func=ast.Name(id=ast_obj.func.attr, ctx=ast.Load()),
                                    args=ast_obj.args,
                                    keywords=ast_obj.keywords)
                self._deque.appendleft(call_obj)
                self.__parse_statement(ast_obj.func.value)
            # In rare cases, even func also can have another function 'tdmlspk_dummy'.
            # In such cases, create another Call object with dummy name.
            # When populating the user guide in such cases, one should look at
            # function name and take call appropriately.
            # Nested function call: func()()
            elif isinstance(ast_obj.func, ast.Call):
                call_obj = ast.Call(func=ast.Name(id="tdmlspk_dummy", ctx=ast.Load()),
                                    args=ast_obj.args,
                                    keywords=ast_obj.keywords)
                self._deque.appendleft(call_obj)
                self.__parse_statement(ast_obj.func)

        elif isinstance(ast_obj, ast.Attribute):
            self._deque.appendleft(ast.Name(id=ast_obj.attr, ctx=ast.Load()))
            self.__parse_statement(ast_obj.value)
        else:
            # Here walk through the ast_obj and extract all names, if attribute then attr,
            # if function then func.id, if name then id and blindly populate the UserNotes.
            for sub_node in ast.walk(ast_obj):
                if isinstance(sub_node, (ast.Name, ast.Attribute)):
                    name = sub_node.id if isinstance(sub_node, ast.Name) else sub_node.attr
                    if self.start_line == self.end_line:
                        if name in ['cast', 'like', 'ilike', 'agg']:
                            self._process_keywords_call_args(ast_obj, name)
                        else:
                            self._process_user_notes(name)
                        self.is_spark_component_involved=True


    def __process_import(self, ast_obj):
        """
        DESCRIPTION:
            Parses the import statement and populates corresponding user notes.

        PARAMETERS:
            ast_obj:
                Required Argument.
                The AST object representing the import statement to be parsed.
                Type: ast.Import or ast.ImportFrom

        RETURNS:
            None
        """
        not_supported = self.tdmlspk_notes.get("not_supported")

        #  Pass ast obj to the _ImportParser class.
        translated_line, invalid_imports, spark_imports = _ImportParser(ast_obj, not_supported).get_imports() 
        if spark_imports:
            self.__spark_imports = self.__spark_imports.union(set(spark_imports))
        # Create UserNotes for all the invalid imports.
        if invalid_imports:
            for import_info in invalid_imports:
                obj_name = import_info['obj']
                notes_ = not_supported[obj_name]
                notes_ = notes_ + "<span style='font-style: italic;'> Import is ignored. </span>"
                if self.cell_no:
                    self._user_notes[obj_name] = NotebookUserNote(self.cell_no, self.start_line, self.end_line, obj_name, notes_, UserNoteType.NO_ACTION)
                else:
                    self._user_notes[obj_name] = UserNote(self.start_line, self.end_line, obj_name, notes_, UserNoteType.NO_ACTION)

        # If line is modified then add that into self.modified_statement.
        if translated_line is not None:
            self.modified_statement = translated_line
                
    def get_user_guide(self):
        """
        DESCRIPTION:
            Retrieves the user guide for the corresponding statement.

        PARAMETERS:
            None

        RETURNS:
            list:
                A list of user notes associated with the statement.
                Each element represents a user note.
                Type: List[UserNote]
        """
        return list(self._user_notes.values()) 
    