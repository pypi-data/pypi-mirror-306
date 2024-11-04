
# pylint: disable=line-too-long

from copy import deepcopy
from typing import Dict, Optional

def provider_preproc_single_symbol_bulk(records_origin_short_ref, original_records, changelog_id:Optional[str]=None, records_category:Optional[str]=None):

    """
    Preprocesses the original records for a single symbol by applying provider-specific transformations.
    This function deep-copies the original records and applies preprocessing steps based on the data source. 
    For example, it can rename the date column to a standard format and document the changes in a description list.
    """

    result = {
        "preprocessed_records": None,
        "preproc_descr": None,
        "original_date_col_name": None
    }

    preproc_descr =[">> Provider-specific preprocessing steps:"]

    copied_original_records = deepcopy(original_records)
    original_date_col_name=None  # Initialize date_col_name

    if records_origin_short_ref == "eodhd__eod":
        original_date_col_name = "date"
        for record in copied_original_records:
            # Directly rename the key within the record
            record['date_id'] = record.pop(original_date_col_name)
        preproc_descr.append(f"-- Renamed '{original_date_col_name}' to 'date_id' --")
        
        result["preprocessed_records"] = copied_original_records
        result["preproc_descr"] = '--'.join(preproc_descr)
        result["original_date_col_name"] = original_date_col_name

        return result

    if records_origin_short_ref == "eodhd__eod_bulk_last_day":
        raise ValueError("Data Origin 'eodhd__eod_bulk_last_day' not supported.")
        # original_date_col_name = "date"
        # for record in copied_original_records:
        #     # Directly rename the key within the record
        #     record['date_id'] = record.pop(original_date_col_name)
        #     record['exchange'] = record.pop('exchange_short_name')
        #     record['symbol']=f"{record['code']}.{record['exchange']}" if record['exchange']!="US" else record['code']
        #     record['exchange'] = record['exchange'] if record['exchange']!="US" else us_code_to_exchange[records_category][record['code']]
        #     record["asset_category"]=records_category
        #     record['datastore_action_id'] = changelog_id
        #     record.pop('code')
        #     record.pop('prev_close')
        #     record.pop('change')
        #     record.pop('change_p')
        # preproc_descr.append(f"--Renamed '{original_date_col_name}' to 'date_id' -- REMOVED 'code', 'exchange_short_name', 'prev_close', 'change', 'change_p' --")
        # return copied_original_records, preproc_descr, original_date_col_name

    raise ValueError(f"Data Origin {records_origin_short_ref} not supported.")


def common_preproc_market_single_symbol_bulk(records_input):

    """
    Applies common preprocessing steps to market data for a single symbol.

    This function processes the input records by rounding the prices to 2 decimal places 
    (3 decimals if the price is less than or equal to 1) and updates the preprocessing description list.
    """
    result = {
        "preprocessed_records": None,
        "preproc_descr": None
    }
    processed_data = []
    preproc_descr = [">> Common preprocessing steps:"]

    ##############################################################
    ########## Define processing helpers #######################

    ################ Round values to save space ###########
    def round_value(value):
        return round(value, 3 if value <= 1 else 2)

    #############################################
    ########## Apply #############################
    for entry in records_input:
        processed_entry = entry.copy()
        # Apply rounding to the numeric fields
        for key in ['open', 'high', 'low', 'close', 'adjusted_close']:
            value = processed_entry.get(key)
            if value is not None:
                processed_entry[key] = round_value(float(value))
        processed_data.append(processed_entry)

    ######### Update preprocessing description to include each step ##########
    preproc_descr.append("Rounded prices to 2 decimals (to 3 decimals if price <=1)")

    result["preprocessed_records"] = processed_data
    result["preproc_descr"] = '--'.join(preproc_descr)

    return result
