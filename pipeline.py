

#This version integrates the single orchestration point of entry (run), explicit exception propagation ( raise), structural inheritance via subclasses, performance tracking decorators, and high-velocity bulking writing via SQLAlchemy into one unified file.


 #Use OS - built-in library that provides a portable way to interact with the underlying operating system. It acts as a bridge, allowing your code to perform system-level tasks like managing files, navigating directories, and accessing environment variables regardless of whether you are on Windows, macOS, or Linux. Like os.getcmd, os.listdir(), or os.makedirs()


import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

from config import Config
from notifications import send_error_email



#Import the structural timing decorator from your local workspace file 
from decorators import log_execution_time           

#Configure local module logger instance - Get logger instance for this specific module
logger = logging.getLogger(__name__)


pd.Timestamp.now()


# =====================================================================
# BASE CLASS: Handles SQL connections, Transformations, Loads & Audits
# =====================================================================
class SQLDataPipeline:
    """
    Baseline Pipeline Class.
    Establishes core structural engineering: handles the database engine --- standard data cleaning transformations, and high-velocity SQL bulk wr Designed to be subclassed based on source formats.
    """

    def __init__ (self, db_url: str, file_path: str):
        self.file_path= file_path
        self.df = None

        try:
            #initialize SQLAlchemy database engine with fast_executemany to enable 
            self.engine = create_engine(
                db_url,
                fast_executemany= True
                )
            
              # Test database connection immediately 
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))


            logger.info("SQLAlchemy database connection engine initialized successfully!")
        except Exception as e:
            logger.critical(
                f"failed to initialize target database engine: {e}"
                )    
            raise


    #====================================================         
    #SINGLE POINT OF ENTRY       
    #====================================================     

    @log_execution_time
    def run(self, table_name: str, **kwargs) -> bool:
        ''' Orchestration Entry Point. Executes the entire end-to-end data pipeline lifecycle sequential.Any keyword arguments (kwargs) pass down cleanly into the reader r '''
        try:
            logger.info(f"Starting pipeline execution loop for table: {table_name}")
                                                                       
            # 1. Ingest Data (Accepts optional args like sheet_name for si)
            self.read_data(**kwargs)

            #2. Mutate / Clean / Transform Data
            self.transform_data()

           #3. Store to Relational target SQL table
            self.load_to_sql(table_name=table_name)

           #4. Final validation Audit Check
            validation_success= self.verify_load(table_name= table_name)

            if validation_success:
                logger.info(f'Pipeline execution lifecycle completed and validated')
            else:
                logger.info(f'Pipeline completed ingestion loop, but validation failed')    
            return validation_success    

        except Exception as e:
            logger.critical(
                f"pipeline execution engine crashed durinf processing: {e}"
                )  
            
            #raise the exception up to main.py to allow final runtime fa
            raise 


    #1 -----------------------------------------------------------------------------------       
    @log_execution_time
    def read_data(self, **kwargs):
        ''' Read a standard delimited csv file into a Pandas dataframe memory. Overridden by specialized child implemenation for a alternate source'''

        try:
            self.df = pd.read_csv(self.file_path,**kwargs)
            logger.info(f"Successfully processed {len(self.df)} raw records")
        except FileNotFoundError as e:
            logger.error(f'Critical operational error: Target csv file missing: {e}')
            raise
        except Exception as e:
            logger.exception(f'Unexpected file system exception reading flat file: {e}')    
            raise


    #2 -----------------------------------------------------------------------------------   
    @log_execution_time
    def transform_data(self):
        ''' Applies standard corporate Pandas validation, format standardization etc'''

        if self.df is None or self.df.empty:
            logger.warning("Pipeline data transformation sequence bypassed - input dataframe is empty")
            return
        try:
            #Structural tansformation :  Clear leading/trailing whitespaces and standardize column names
            self.df.columns = [str(c).strip().lower() for c in self.df.columns]

            #Structural tansformation :  Inject a unified batch metadata
            #self.df['processed_at']= pd.Timestamp.now()
            self.df['report_date']= pd.Timestamp.now()   

            logger.info('Panda system matrix data normalization routines completed successfully!')
        except Exception as e:
            logger.exception(f"Data manipultion sequence crashed during core transformation: {e}")    
            raise

    #3 -----------------------------------------------------------------------------------   
    #3 ------------------New -----------------------------------------------------------------   
    # @log_execution_time
    # def load_to_sql(self, table_name: str):
    #     '''Streams buffer memory blocks directly down into target database using stable Pandas core insertion'''

    #     if self.df is None or self.df.empty:
    #         logger.error(f"Database insertion aborted: No valid local in-memory dataset available")
    #         return
        
    #     # 1. Strip the audit tracking column to match table expectations
    #     if 'processed_at' in self.df.columns:
    #         self.df = self.df.drop(columns=['processed_at'])
            
    #     try:


    #         engine = create_engine(Config.DB_URL,fast_executemany= True)    
    #         self.df.to_sql(table_name,
    #                 schema='JDE_DB_ALAN',    # You have already include schema arguement if your table is not the default dbo schema
    #                 con=engine,
    #                 if_exists='replace',      #change to 'append' if needed
    #                 index = False,
    #                 chunksize=1_000          # Recommended for large datasets

    #                 )
                
    #         logger.info(
    #             f'Successfully loaded and committed dataframe array '
    #             f'{len(self.df)} records into table: {table_name}'
    #         )   
    #     except Exception as e:
    #         logger.exception(f'Database target data bulk storage mapping failure {e}')
    #         raise

    
    #3 ----------------Old working Now - Yeah !-------------------------------------------------------------------   
    @log_execution_time
    def load_to_sql(self, table_name: str):
        '''Streams buffer memory blocks directly down into target database using SQLAlchemy'''

        if self.df is None or self.df.empty:
            logger.error(f"Database insertion aborted: No valid local in-memory dataset available")
            return
        
        if 'processed_at' in self.df.columns:
            self.df = self.df.drop(columns=['processed_at'])

         # SIMPLE & FAST FIX: Automatically aligns data types and missing values cleanly
        # This keeps your code brief while allowing fast_executemany to run at full speed!
        self.df = self.df.convert_dtypes()
        self.df = self.df.where(self.df.notna(), None)


        #debug check: Let's us see if the dataframe actully has rows right here     
        print(f"--- Debug: Dataframe shape is {self.df.shape} ---")
        num= self.df.head(23)           # column 23 is 'reorder_qty_max'
                                        #The function self.df.head(2) does not pull out a single row. Instead, it creates a brand new table (DataFrame) containing the top two rows of your data, along with all of its original columns and headers.
                                        #Because num is still a full table object, Python gets confused when you try to apply a number format to it.
        # Below will not work
        #print(f"{num:_}")

        #1. This will work - # Drop the ":_" modifier entirely to let pandas print the table layout
        print(num)

        #2. Or Extracts a single raw number from the dataframe
        single_value = self.df.iloc[1, 23] 
        print(f"{single_value:_}")

        #3. Or Select the 2nd column (index 1) and map the underscore format to every row
        #self.df.iloc[:, 23] = self.df.iloc[:, 23].map('{:_}'.format)       # error
        self.df.iloc[:, 23] = self.df.iloc[:, 23].fillna(0).map('{:_}'.format)
        # Now print the head of the dataframe to see the formatted column
        print(self.df.head(23))

        #4-1.  Create a temporary display column without touching the original dataframe
        preview = self.df.iloc[:, 23].fillna(0).map('{:_}'.format)
        # 4-2. Print the temporary preview to your console
        print(preview.head(23))
        # Your original self.df remains 100% clean and ready for SQL!


        
        #create a new df and Apply underscore formatting to the column 'Large_num' - This transformation turns your numbers into text (strings). Once you run this line, you can no longer perform math operations (like addition or averaging) on this column.
        #df = pd.DataFrame({'large_num': [1000000, 2500000, 3750000]})
        #df['large_num'] = df['large_num'].apply(lambda x: f"{x:_}"

        # Format the display with underscores - Preserves Math: The underlying values remain int or float. You can still run df['large_num'].sum() or df.describe().
        #df.style.format({'large_num': '{:_}'})
        
        try:
            #Use begin() context manager to auto-commit when the code in/ for transaction auto-commit
            with self.engine.begin() as connection:

                # FIX: Force the underlying pyodbc connection to utilize fast_executemany bulk copy.
                # This completely bypasses the driver's internal buggy Unicode conversion buffers.
               # connection.connection.fast_executemany = True

                self.df.to_sql(
                    name= table_name,
                    schema='JDE_DB_ALAN',  # <-- THIS IS CRITICAL FOR 'replace' TO WORK
                    #con=connection,
                    con=self.engine,
                    if_exists='replace',
                    index= False,
                    chunksize = 1000        #buffers data over the wire in segment

                )

                # FORCE SQL SERVER TO FLUSH DATA TO DISK IMMEDIATELY:
                connection.commit() 
                
            logger.info(
                    f'Successfully loaded and committed dataframe array'
                    f'{len(self.df)} records into table: {table_name}'
                  )   
        except Exception as e:
            logger.exception(f'Database target data bulk storage mapping failure {e}')

            # 2. CALL THE STANDALONE FUNCTION HERE (No "self." needed)
            send_error_email(error_message=str(e), table_name=table_name)

            raise


    #4 ----- new  ------------------------------------------------------------------------------
    @log_execution_time
    def verify_load(self, table_name: str) -> bool:
        ''' Post-load analytical check verifying that data rows are accessible from the target table.'''
        try:
            with self.engine.connect() as connection:
                # 1. Structural Fix: Match your targeted database schema explicitly
                query = text(f"SELECT COUNT(*) FROM JDE_DB_ALAN.{table_name}")
                
                # 2. Logic Fix: Extract the scalar integer value out of the query block
                row_count = connection.execute(query).scalar()
            
            # Evaluate the raw count instead of checking if the dataframe is empty
            records_exist = int(row_count) > 0
            
            if records_exist:
                logger.info(f"Verification success: Confirmed {row_count} records inside table: JDE_DB_ALAN.{table_name}")
            else:
                logger.warning(f"Verification warning: Target table JDE_DB_ALAN.{table_name} is empty.")
                
            return records_exist
        
        except Exception as e:
            logger.exception(f"Post-execution verification check failed on load validation: {e}")
            raise # Kept your 'raise' pattern intact to bubble up to main.py execution loop



    #4 ----- old ------------------------------------------------------------------------------   
    #The Bug: Your SQL query executes a SELECT COUNT(*) FROM table.
    #The Problem: Even if your destination database table contains 0 rows, the database engine will still return an active dataset containing a single row with the number 0. Because pandas captures this single row, test_df.empty will always evaluate to False (meaning records_exist evaluates to True).
    #The Result: Your verification step will incorrectly report a successful load even if the target table is completely empty.
    """
    @log_execution_time
    def verify_load(self, table_name: str) -> bool:
        ''' Post-load analytical check verifying that data rows are accessible from the target table.'''

        try:
            with self.engine.connect() as connection:
                query = text(
                           # f"Select top 5 * from {table_name}"
                              f"Select count(*) from JDE_DB_ALAN.{table_name}"
                            )
                test_df = pd.read_sql(
                            query,
                            connection
                            )
            
            records_exist = not test_df.empty
            if records_exist:
                logger.info(
                    f"Verification success: confirmed accessible "
                    f"records in target table: {table_name}"
                    )
            else:
                logger.warning(
                    f"Verification warning: target table "
                    f"{table_name} returned zero records"
                    )
            return records_exist
        
        except Exception as e:
            logger.exception(
                    f"Post-execution verification check failed "
                    f"on load validation: {e}"
                    )
        raise
    """    
    


# =====================================================================
# SUBCLASS: Specialized only for Excel Extraction
# =====================================================================

class ExcelDataPipeline(SQLDataPipeline):
    '''
    Excel subclass
    Inherits database mechanics,transformations, validation, and metrics
    Overrides solely the read_data signature block to swap out flat-file parsing for Excel ingestion.
    '''

    @log_execution_time
    def read_data(self, **kwargs):
       # return super().read_data(**kwargs)     -- "Run the parent class read_data() method" - no need here as child read Excel not Csv
       '''
       Reads target Excel worksheets into standard dataframe arrays.
       Accepts parameters like sheet_name through kwargs.
       ''' 
       try:
         #Extract sheet_name if provided, defaulting to the first sheet
        #sheet_name= kwargs.get('sheet_name',0)     -- better version below, BUT you never used sheet_name. Below inserts default only if missing, and avoids duplicate parameter issue. Very elegant Python approach.
        kwargs.setdefault("sheet_name",0)
        self.df = pd.read_excel(
                self.file_path,
                **kwargs)
        
        logger.info(f'Successfully processed {len(self.df)} worksheet')
      
       except FileNotFoundError as e:
        logger.error(f"Critical operational error: Target binary Excel -- {e}")   
        raise
       
       except Exception as e:
        logger.exception(f"Unexpected Excel parsing exception -- {e}")
        raise
           


# =====================================================================
# FACTORY: Dynamic Router Switchboard
# =====================================================================
#In real factory, you(consumer) don't need to know the raw machinery, assembly tools, or complex steps rquired to build a product.You simple request an item, and the factory takes care of the internal manufacturing steps and hands you a finished product.
#In software engineering, the pattern works exactly the same way:
#1. It decouples 'Creation' from 'Use' - instead of your main program ( main.py) manually figuring out how to build and configure different pipelines using complex if/else logic, it offloads that resposibility to a dedicated work project: The Factory.
#2. Standardized Outputs - Just like a real car factory might produce different models of cars ( Sedans, SUVs, trucks) that all share the same steering wheel or pedals, your code factory produces different pipeline objects ( SQLDatapipe or ExcelDatapipe) that all share the exact same interface ( the .run() method ).
# Why this design is powerful:
#If next week your company tells you that you now need to fetch data from a JSON API endpoint, you only need to create a third subclass: class JsonApiPipeline(SQLDataPipeline): and add an elif extension == '.json': line to the factory. Your main.py core engine won't need to change a single line of code!
#Yes, the approach you are thinking of is exactly what the Factory Pattern achieves.
#By combining your Object-Oriented (OOP) subclasses with a Factory class, Python will inspect the file extension (.csv vs .xlsx) at runtime and automatically hand back the correct pipeline object. This keeps your main.py completely clean because you don't need if/else statements repeated everywhere.
#Here is exactly how to structure the Base class, Subclasses, and the Factory to handle this dynamically.
#Verification Check for this Step
#To ensure this runs smoothly when you execute it, verify two small things in your pipeline.py file:
#Make sure you have import os at the very top of your pipeline.py file so that os.path.splitext works without throwing a NameError.
#Ensure that ExcelDataPipeline and SQLDataPipeline are both defined above or in the same scope as this factory class.

#Enhancement made to Modify your PipelineFactory.get_pipeline method to return a two-item tuple: (pipeline_object, extension_string).
# You are 100% correct. That is exactly how it works under the hood.
# In Python, whenever you put a comma between items in a return statement (like return pipeline_obj, extension), Python automatically wraps them up together into a single tuple object behind the scenes.
# A tuple is the perfect data container here because it can hold mixed data types—in this case, an instantiated object instance as the first element and a raw string as the second element.
# How main.py Unpacks the Package
# When this tuple arrives in main.py, you use tuple unpacking to split those two elements back apart instantly into individual variables:
# pipeline, extension = PipelineFactory.get_pipeline(db_url=Config.DB_URL, file_path=file_path)
#Python calls the factory method.
#The factory returns the single tuple package.
#Python splits the package: it looks inside index 0, pulls out the live object, and assigns it to pipeline. Then it looks inside index 1, pulls out the string, and assigns it to extension.
#Your understanding of this structural mechanic is spot on. You have cleanly separated your program's architectural layers.

class PipelineFactory:
    """ Inspect file extensions to return the correct instantiated pipeline pipeline object. """

    @staticmethod
    def get_pipeline(db_url: str, file_path: str) -> tuple[SQLDataPipeline, str]:

        '''Inspects string signatures and instantiates the correct subclass asset. Returns a tuple matching: (PipelineInstance, ExtensionString) '''        
        '''Extract the extension (e.g., '.csv' or '.xlsx') and force lowercase '''
        if not file_path:
            raise ValueError("Factory initialization failed: Target file path is empty or null.")
    
        # 1. Extract the extension once, right here inside the switchboard and Strip out the leading dot (e.g., '.xlsx' becomes 'xlsx') to ensure matching profiles
        _,raw_extension = os.path.splitext(file_path.lower())
        extension = raw_extension.replace('.','').strip()

        # 2. Build the correct object instance based on that extension
        if extension in ['xlsx','xls']:
            logger.info(f"Factory detected Excel file type for path: { file_path}")

            pipeline_obj = ExcelDataPipeline(db_url,file_path)
        
        elif extension in ['csv','txt']:
            logger.info(f"Factory detected CSV/Flat file type for path: {file_path} ")

            pipeline_obj = SQLDataPipeline(db_url,file_path)
        else:
            raise ValueError(f"Unsupported file extension context: {extension}")
        
        # 3. Returns BOTH initialized object and the extension string as a tuple to main()
        return pipeline_obj, extension
     
  

    '''
    @staticmethod
    def get_pipeline_old(db_url: str, file_path: str) -> SQLDataPipeline:

        #Extract the extension (e.g., '.csv' or '.xlsx') and force lowercase      
        _,extension = os.path.splitext(file_path.lower())
       
        if extension in ['xlsx','xls']:
            logger.info(f"Factory detected Excel file type for path: { file_path}")
            return ExcelDataPipeline(db_url,file_path)
        
        elif extension in ['csv','txt']:
            logger.info(f"Factory detected CSV/Flat file type for path: {file_path} ")
            return SQLDataPipeline(db_url,file_path)
        else:
            raise ValueError(f"Unsupported file extension context: {extension}")
            
    '''