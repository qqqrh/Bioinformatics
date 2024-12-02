import requests, json, pandas as pd, time

def get_gene_info(gene_id):
    # gene id is str
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
    df = pd.read_csv(csv_file)
    global n
    n = input("How many do you want to analyze: ")
    gene_exp = []
    
    # Read first n rows
    for i in range(min(int(n), len(df))):
        gene_id = df.iloc[i, 0]  # gene id is the first column
        expression_value = df.iloc[i, -1]  # gene expression is the last column
        gene_exp.append((gene_id, expression_value))

    # Read last n rows
    for i in range(max(0, len(df)-int(n)), len(df)):
        gene_id = df.iloc[i, 0]
        expression_value = df.iloc[i, -1]
        gene_exp.append((gene_id, expression_value))
    
    return gene_exp

def main():
    csv_file = input("Please input the csv file: ")
    gene_exp = read_gene_expression(csv_file)
    output_data = []
    cnt = 0
    
    for gene_id, expression_value in gene_exp:
        # print(f"Gene ID: {gene_id}, Expression Value: {expression_value}")
        gene_info = get_gene_info(gene_id)
        
        if gene_info:
            # print("\nGene Information: ")
            # print(json.dumps(gene_info, indent=4))
            gene_name = gene_info.get("display_name", "N/A")
            gene_description = gene_info.get("description", "N/A")
            if gene_name == "N/A" and "novel" in gene_description.lower():
                gene_name = "novel gene"
            if (gene_id, gene_name) not in [(x[0], x[2]) for x in output_data]:
                output_data.append([gene_id, expression_value, gene_name, gene_description])
    
    # Write output to csv
    output_df = pd.DataFrame(output_data, columns=["Gene ID", "Expression Value", "Gene Name", "Gene Description"])
    output_csv_file = "gene_exp_output.csv"
    output_df.to_csv(output_csv_file, index=False)
    print(f"Output written to {output_csv_file}")

if __name__ == "__main__":
    main()

        