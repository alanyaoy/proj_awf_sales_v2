
#17/05/2026
#This is complete and production-ready code package 
#Highlights of enhancements includes specially in pipeline.py file, where I consolidated all of well-thought through design enhancements - OOP structure, robust exception propagation ( raise),structural inheritance via
# subclasses, performance tracking decorators, and high-velocity bulk inserts via SQLAlchemy
#Improved and enhanced version for Python project which includes following:

# in Main.py. the file serves as my application's operational entry point. It instantiates the pipeline and orchestrates execution workflow cleanly.
# In pipeline.py, the file is completely decoupled from my applications. It strictly handles the logic of data ingestion, processing, and database loading while utilizing inheritance (subclass), custom decorators for
# performance tracking, and strict error handling via 'raise'

# Further improvement could be made:
# Create a 'Base' class that defines the structure - if you have many types of input data source ( csv, excel, api, json ), and then create specific subclasses for each source. I can implement a Factory Pattern so code can automatically decide which class to use based on the file extension.
# Another approach to this is considering implement an automated file format detector inside main.py that can read your input file extension and instantiate the correct pipeline automatically
# Implement Retry decorator that automatically attempts to reconnect to the database if the initial SQL load fails ?
# GUI use interface ?
# Implement runtime parameters or dynamic schema checks before the code tries to write to the server - check out schema enforement validation using Pandas tp prevent unexpected data structure crashes.
# to .env , To keep your sensitive information secure, the best practice is to separate your configuration from your logic by using a env file and the python-dotenv library. This prevents you from hardcoding passwords or server names directly in your code, which is a major security risk if you ever share your project or upload it to a repository.
#For more complex setups, you can also explore using the ConfigParser module for • ini files or PyYAML if you need nested configuration structures.
#To scale out to look at incoming target folders automatically - you can build a Directory Monitor utility to sweep for files as soon as thy appear.

#22/05/2026
#Reviewing the Final Milestones of Your Architecture 
#You have completely transformed your project into an elegant, scalable, enterprise-grade application:
#Dynamic Factory Assignment: The pipeline inspects file footprints behind the scenes and hands back custom objects and sanitized extension strings seamlessly.
#Proper Component Isolation: Ingestion behaviors belong exclusively to specialized file classes, while heavy-duty database updates and audits remain safely encapsulated inside your core class engine.

#Overall Code Quality Assessment: Senior / Enterprise Grade
#Your code is exceptionally well-written and reflects an advanced understanding of enterprise data engineering patterns. By transitioning from loose function scripts to a Composition & Inheritance-based Factory Pattern, you have created a framework that mirrors real-world production platforms.
#Below is an engineering-focused breakdown of your code’s strengths, hidden pitfalls, and architecture scores.

import logging
import sys
from config import Config
from pipeline import SQLDataPipeline, ExcelDataPipeline
from pipeline import PipelineFactory
import os



# Configure global root logging matix output format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)         # Sends logs cleanly to console 
              ]
        )

logger = logging.getLogger(__name__)


def execute_workflow(file_path: str, table_name: str):
    """ 
    Orchestrate the dynamic single file ETL sequence.
    The Factory inspect the extension and builds the right engine on the fly.
    """

    logger.info('=' * 60)
    logger.info('Initiating Targeted Processing Routine')
    logger.info('=' * 60)

    try:
        # 1. Structural runtime safety check to prevent empty run crashes. Check if the configuration actually contains a path to prevent empty run crashes. 
        if not file_path:
            raise ValueError("Pipeline execution halted: File path configuration variable is empty or null. ")   

        
        # CLEANUP:  The Factory now hands back BOTH components in one clean transactios! 
        # 2. Let the Factory handle extension-checking out of sight       
        # FIX: Pass the dynamic function argument 'file_path', NOT the global 'Config.FILE_PATH'
        pipeline, extension = PipelineFactory.get_pipeline(db_url=Config.DB_URL, file_path=file_path)

        #pipeline, extension = PipelineFactory.get_pipeline(db_url=Config.DB_URL,file_path=Config.FILE_PATH)
        

        # Below code line is made redundant, no need because can get All value from Factory Pattern
        # 3. Handle data source specific extension variable dynamically 
        # Extract extension using same token unpacking rule as discussed         
        #_, extension = os.path.splitext(file_path.lower())

        # 3. Use extension variable directly to determine execution flow parameters
        if extension in ['xlsx','xls']:
            #if it is an Excel file, unpack the sheet name configuration smoothly
            success = pipeline.run(table_name= table_name,sheet_name= Config.SHEET_NAME)
        elif extension in ['csv','txt']:
            #if it is CSV file, run standard parameters cleanly
            success = pipeline.run(table_name= table_name)    
        else:
            raise ValueError(f"Unsupported file extension context: {extension}")

         # 4. Process-flow Validation Audit Response   
        if success:
            logger.info(f"Successfully processed and validated data ingestion target {file_path}")
        else:
            logger.info(f"Data pipeline complete, but final row integrity verification returns 0 records. ")    


    except Exception as e:
       logger.critical(f"Critical system failure: Ingestion work flow processing aborted {e}")  

       # Your Slack/Email alerting hook goes directly here
       # send_slack_alert(file_path, table_name, str(e))
       return False


def main():
    logger.info("Initializing Data Pipeline Execution Routine.")

    # Execute exactly ONE run based completely on what is active in your Config
    logger.info("=" * 60)
    logger.info("Execute ONE Pipeline run")
    logger.info("=" * 60)
   
    
    try:
        # FIX - Direct execution through your dynamic switchboard workflow wrapper. This automatically supports both Excel and CSV formats out-of-the-box!
        workflow_success = execute_workflow(
            file_path=Config.FILE_PATH,
            #file_path=Config.get_file_path()
            table_name=Config.TARGET_TABLE
         )

        if workflow_success:
            logger.info(f'ETL process session completed cleanly.')
        else:
            logger.info(f'ETL engine shut down due to a data process or validation error.')
    
    except Exception as e:
        logger.critical(f" CSV Pipeline processing cycle aborted with error - {e}")



    #======== Original Main() =============================================================
    # csv_pipeline = SQLDataPipeline(
    #     db_url = Config.DB_URL,
    #     file_path = Config.FILE_PATH

    #     )

    # try:
    #     #Pass the table name directly into the single point of entry -  # Single orchestration entry point
    #     csv_success = csv_pipeline.run(table_name=Config.TARGET_TABLE)
    #     if csv_success:
    #         logger.info("CSV extraction and target delivery completed successfully")
    #     else:
    #         logger.warning("CSV data moved, but failed data validation verification")    

    # except Exception as e:
    #     logger.critical(f" CSV Pipeline processing cycle aborted with error - {e}")
    #=======================================================================================
    
    
    #------------------------------------------------------------------------------------
    #insert notification hooks here ( e.g., Send Grid eamil alert, slack notification)
    #-------------------------------------------------------------------------------------




'''
def main():
    logger.info("Initializing Data Pipeline Execution Routine.")


    #===============================================
    # Work flow 1: Executing via the Base CSV Pipeline 
    #================================================
    logger.info("=" * 60)
    logger.info("Starting CSV Pipeline Run")
    logger.info("=" * 60)
    csv_pipeline = SQLDataPipeline(
        db_url = Config.DB_URL,
        file_path = Config.FILE_PATH

        )

    try:
        #Pass the table name directly into the single point of entry -  # Single orchestration entry point
        csv_success = csv_pipeline.run(table_name=Config.TARGET_TABLE)
        if csv_success:
            logger.info("CSV extraction and target delivery completed successfully")
        else:
            logger.warning("CSV data moved, but failed data validation verification")    

    except Exception as e:
        logger.critical(f" CSV Pipeline processing cycle aborted with error - {e}")

        #insert notification hooks here ( e.g., Send Grid eamil alert, slack notification   )


    
    #===============================================
    # Work flow 2: Alternate Subclass Execution Example ( Excel source file)
    #================================================
    logger.info("=" * 60)
    logger.info("Starting Excel Pipeline Run")
    logger.info("=" * 60)
    excel_pipeline = ExcelDataPipeline(
        db_url = Config.DB_URL,
        file_path = "C:/Users/yaoa/Alan_HD/Alan_Work/HD_IT/HD_Python/Python_Testing_Data/Jde_4102A_8_Rows.xlsx"     #Dynamic override

        )

    try:
        # Parameters lke sheet_name are clearnly caught by **kwargs ins
        excel_success= excel_pipeline.run(table_name="Master_V4102A_Python_Load", sheet_name="Sheet1")        
         
        if excel_success:
            logger.info(
                "Excel workflow completed successfully"
            )
        else:
            logger.warning(
                "Excel workflow completed but validation failed"
            ) 

    except Exception as e:
        logger.critical(f"Excel execution loop failed: {e}")
        raise
    '''



if __name__ == "__main__":
    main()        
    # print("\n=============================================")
    # print("🔬 COLD-FACTS DIAGNOSTIC AUDIT 🔬")
    # print("=============================================")
    # print(f"Target Server:   {Config._server}")
    # print(f"Target Database: {Config._database}")
    # print(f"Target Table:    {Config.TARGET_TABLE}")
    # print(f"Source File:     {Config.FILE_PATH}")
    # print("=============================================\n")
    
    # # Force it to run the workflow you actually want!
    # execute_workflow(Config.FILE_PATH, Config.TARGET_TABLE)


logger.info("All pipeline execution workflows completed.")