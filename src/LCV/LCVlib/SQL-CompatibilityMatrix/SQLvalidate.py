#!/usr/bin/python
import psycopg2
import pandas as pd
import numpy as np
from config import config
orLater = "or-later"


def postgresql_to_dataframe(conn, column_names_list):
    """
    Tranform a SELECT query into a pandas dataframe
    """

    cursor = conn.cursor()
    select_query = "SELECT %s FROM validationmatrix" % (
        ', '.join('"' + item + '"' for item in column_names_list))

    try:
        cursor.execute(select_query, column_names_list)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names_list)
    return df


def CSV_to_dataframe(CSVfilePath, column_names_list):
    """
    Import a CSV and transform it into a pandas dataframe
    """
    df = pd.read_csv(CSVfilePath, usecols=column_names_list)

    return df


def SPDXIdMapping(license_list_cleaned):
    CSVfilePath = "spdx-id.csv"
    license_list_SPDX = []
    column_names_list = ['Scancode', 'SPDX-ID']
    df = CSV_to_dataframe(CSVfilePath, column_names_list)
    df = df.set_index('Scancode')
    for license in license_list_cleaned:
        newElement = df.loc[license]['SPDX-ID']
        # print(newElement)
        if newElement is not np.nan:
            license_list_SPDX.append(newElement)
            if orLater in newElement:
                print("The usage of 'or later' is not supported. \n Please specify a license version instead of using 'or later' notation.")
                exit(0)
        else:
            license_list_SPDX.append(license)
    return license_list_SPDX


def validate(license_list_cleaned, OutboundLicense):
    """ Connect to the PostgreSQL database server OR read from CSV """
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # CSVfilePath = "licenses.csv"

        # duplicating the list to compare items, and before adding License field
        # license_list_cleaned_to_compare = license_list_cleaned

        # USED TO COMPARE INBOUND LICENSES
        column_names_list = license_list_cleaned.copy()

        column_names_list = [OutboundLicense]
        column_names_list.insert(0, 'License')

        # retrieve data from PostgreSQL
        df = postgresql_to_dataframe(conn, column_names_list)

        # retrieve data from CSV file
        # df = CSV_to_dataframe(CSVfilePath, column_names_list)
        df = df.set_index('License')
        if (len(license_list_cleaned) == 1) and (license_list_cleaned[0] == OutboundLicense):
            print("For this project only "
                  + license_list_cleaned[0]+" as the inbound license has been detected, and it is the same of the outbound license ("+OutboundLicense+"). \nIt means that it is license compliant. ")
            exit(0)

            verificationList = list()

            for license in license_list_cleaned:
                comparison = df.loc[license, OutboundLicense]
                if comparison == "0":
                    output = license+" is not compatible with " + \
                        OutboundLicense+" as an outbound license."
                    # print(output)
                    verificationList.append(output)

                else:
                    output = license+" is compatible with " + \
                        OutboundLicense + " as an outbound license."
                    # print(output)
                    verificationList.append(output)
            return verificationList

            # THIS WAS USED TO COMPARE INBOUND LICENSES --> STILL USEFUL TO DETECT INBOUND LICENSES INCOMPATIBILITY
            # for license in license_list_cleaned:
            #     for license_to_compare in license_list_cleaned_to_compare:
            #         comparison = df.loc[license,license_to_compare]
            #         # print(comparison)
            #         if comparison == "0" :
            #             # print("hello")
            #             print(license+" is not compatible with "+license_to_compare)

        # postgresql_to_dataframe related code
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# if __name__ == '__main__':
#     connect()
