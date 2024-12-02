import requests, json, pandas as pd, time

def get_gene_id(gene_name):
    server = "https://rest.ensembl.org"
    endpoint = f"/xrefs/symbol/homo_sapiens/{gene_name}?"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(server + endpoint, headers=headers)
        if not response.ok:
            print(f"Failed to fetch information for Gene Name: {gene_name}")
            return None
        return response.json()[0]['id'] if response.json() else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Gene Name {gene_name}: {e}")
        return None
    finally:
        time.sleep(0.5)

def get_gene_info(gene_id):
    server = "https://rest.ensembl.org"
    endpoint = f"/lookup/id/{gene_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(server + endpoint, headers=headers)
        if not response.ok:
            print(f"Failed to fetch information for Gene ID: {gene_id}")
            return None
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Gene ID {gene_id}: {e}")
        return None
    finally:
        time.sleep(0.5)

def read_gene_expression(csv_file):
    # Read the CSV with explicit data types to prevent truncation issues
    df = pd.read_csv(csv_file, dtype={'Expression Value': float})
    return df

def main():
    csv_file = input("Please input the csv file: ")
    gene_names = input("Please input one or more gene names (separated by a comma): ").split(",")
    gene_names = [gene.strip() for gene in gene_names]
    
    df = read_gene_expression(csv_file)
    output_data = []
    
    for gene_name in gene_names:
        gene_id = get_gene_id(gene_name)
        if gene_id:
            matching_rows = df[df.iloc[:, 0] == gene_id]
            if not matching_rows.empty:
                for index, row in matching_rows.iterrows():
                    # Ensure the expression value is correctly read as float
                    expression_value = float(row.iloc[-1])  
                    gene_info = get_gene_info(gene_id)
                    if gene_info:
                        gene_description = gene_info.get("description", "N/A")
                        output_data.append([gene_id, index + 1, gene_name, expression_value, gene_description])
            else:
                print(f"Gene ID {gene_id} for gene name {gene_name} not found in the CSV file.")
        else:
            print(f"Gene Name {gene_name} could not be found in Ensembl.")
    
    # Write output to csv
    output_df = pd.DataFrame(output_data, columns=["Gene ID", "Ranking in CSV", "Gene Name", "Expression Value", "Gene Description"])
    import os

    output_csv_file = os.path.join(os.path.dirname(csv_file), "gene_search.csv")
    output_df.to_csv(output_csv_file, index=False)
    print(f"Output written to {output_csv_file}")
    print(output_df)

if __name__ == "__main__":
    main()
