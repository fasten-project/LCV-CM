df = CSV_to_dataframe(CSVfilePath, column_names_list)
Column_array = df.to_numpy()


if (license in Column_array):


else:
        output = ""+license+" is not present in the Compatibility Matrix"
        verificationList.append(output)
