from __future__ import print_function
from __future__ import unicode_literals
import sys
import logging
import datetime
import dateutil
import uploader
import utilities
import formatter
import postprocess
import oneaday_filter
import result_formatter
import scraper_connection
import to_mongo
from petrarch import petrarch


def main(file_details, server_details, logger_file=None, run_filter=None,
         run_date=''):
    """
    Main function to run all the things.

    Parameters
    ----------

    file_details: Named tuple.
                    All the other config information not in ``server_details``.

    server_details: Named tuple.
                    Config information specifically related to the remote
                    server for FTP uploading.

    logger_file: String.
                    Path to a log file. Defaults to ``None`` and opens a
                    ``PHOX_pipeline.log`` file in the current working
                    directory.

    run_filter: String.
                Whether to run the ``oneaday_formatter``. Takes True or False
                (strings) as values.

    run_date: String.
                Date of the format YYYYMMDD. The pipeline will run using this
                date. If not specified the pipeline will run with
                ``current_date`` minus one day.
    """
    if logger_file:
        utilities.init_logger(logger_file)
    else:
        utilities.init_logger('PHOX_pipeline.log')
    # get a local copy for the pipeline
    logger = logging.getLogger('pipeline_log')

    print('\nPHOX.pipeline run:', datetime.datetime.utcnow())

    if run_date:
        process_date = dateutil.parser.parse(run_date)
        date_string = '{:02d}{:02d}{:02d}'.format(process_date.year,
                                                  process_date.month,
                                                  process_date.day)
        logger.info('Date string: {}'.format(date_string))
        print('Date string:', date_string)
    else:
        process_date = datetime.datetime.utcnow() - datetime.timedelta(days=0)
        date_string = '{:02d}{:02d}{:02d}'.format(process_date.year,
                                                  process_date.month,
                                                  process_date.day)
        logger.info('Date string: {}'.format(date_string))
        print('Date string:', date_string)

    results, scraperfilename, story_collection = scraper_connection.main(process_date,
                                                       file_details)

    if scraperfilename:
        logger.info("Scraper file name: " + scraperfilename)
        print("Scraper file name:", scraperfilename)

    logger.info("Running Mongo.formatter.py")
    print("Running Mongo.formatter.py")
    formatted = formatter.main(results, file_details,
                               process_date, date_string)

    logger.info("Running PETRARCH")
    file_details.fullfile_stem + date_string
    if run_filter == 'False':
        print('Running PETRARCH and writing to a file. No one-a-day.')
        logger.info('Running PETRARCH and writing to a file. No one-a-day.')
        #Command to write output to a file directly from PETR
#        petrarch.run_pipeline(formatted,
#                              '{}{}.txt'.format(file_details.fullfile_stem,
#                                                date_string), parsed=True)
        petr_results = petrarch.run_pipeline(formatted, write_output=False,
                                             parsed=True)
    elif run_filter == 'True':
        print('Running PETRARCH and returning output.')
        logger.info('Running PETRARCH and returning output.')
        petr_results = petrarch.run_pipeline(formatted, write_output=False,
                                             parsed=True)
    else:
        print("""Can't run with the options you've specified. You need to fix
              something.""")
        logger.warning("Can't run with the options you've specified. Exiting.")
        sys.exit()

    if run_filter == 'True':
        logger.info("Running oneaday_formatter.py")
        print("Running oneaday_formatter.py")
        formatted_results = oneaday_filter.main(petr_results)
    else:
        logger.info("Running result_formatter.py")
        print("Running result_formatter.py")
        formatted_results = result_formatter.main(petr_results)

    logger.info("Running postprocess.py")
    print("Running postprocess.py")
    postprocess.main(formatted_results, date_string,
                     file_details, server_details)

    logger.info("Running phox_uploader.py")
    print("Running phox_uploader.py")
    try:
        uploader.main(date_string, server_details, file_details)
    except Exception as e:
        logger.warning("Error on the upload portion. {}".format(e))
        print("""Error on the uploader. This step isn't absolutely necessary.
              Valid events should still be generated.""")

    logger.info("Updating story collection to set phoenix = 1")
    print("Updating story collection to set phoenix = 1")
    #here's a stab at the update part; needs to be tested
    for i, story in enumerate(list(results)):
         story_collection.update({"_id": story['_id']},{"$set": {"phoenix": 1}})
    
    logger.info('PHOX.pipeline end')
    print('PHOX.pipeline end:', datetime.datetime.utcnow())


if __name__ == '__main__':
    # initialize the various utilities globals
    server_details, file_details = utilities.parse_config('PHOX_config.ini')

    while 1:
         main(file_details, server_details, file_details.log_file, run_filter=file_details.oneaday_filter)
         to_mongo.main()
         yesterday_date = datetime.datetime.utcnow() - datetime.timedelta(days=1)
         yesterday_date_string = '{:02d}{:02d}{:02d}'.format(yesterday_date.year, yesterday_date.month, yesterday_date.day)
         main(file_details, server_details, file_details.log_file, run_filter=file_details.oneaday_filter, run_date = yesterday_date_string)
         to_mongo.main()
    #may want to re-run main on one day previous in case events that show up in the database just before midnight are not caught
