"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
from pathlib import Path
import zipfile

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months

    """

    # Definir rutas:
    input_folder = Path("files/input/")
    output_folder = Path("files/output/")

    # Crear carpeta de salida si no existe:
    output_folder.mkdir(parents=True, exist_ok=True) 

    # Leer los archivos comprimidos:
    zip_files = list(input_folder.glob("*.zip"))


    dataframes = []
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file) as z:
            for csv_file in z.namelist():
                if csv_file.endswith(".csv"):
                    dataframes.append(pd.read_csv(z.open(csv_file)))

    # Combinar los dataframes:
    data = pd.concat(dataframes, ignore_index=True)

    # Limpieza y creación de los archivos
    # Client data
    client = data[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    client['job'] = client['job'].str.replace('.', '', regex=False).str.replace('-', '_', regex=False)
    client['education'] = client['education'].str.replace('.', '_', regex=False).replace("unknown", pd.NA)
    client['credit_default'] = client['credit_default'].apply(lambda x: 1 if x == "yes" else 0)
    client['mortgage'] = client['mortgage'].apply(lambda x: 1 if x == "yes" else 0)

    # Campaign data
    campaign = data[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
    campaign['previous_outcome'] = campaign['previous_outcome'].apply(lambda x: 1 if x == "success" else 0)
    campaign['campaign_outcome'] = campaign['campaign_outcome'].apply(lambda x: 1 if x == "yes" else 0)
    campaign['last_contact_date'] = pd.to_datetime(campaign['day'].astype(str) + '-' + campaign['month'] + '-2022', format='%d-%b-%Y')
    campaign = campaign.drop(columns=['day', 'month'])

    # Economics data
    economics = data[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()


    # Guardar los archivos:
    client.to_csv(output_folder / "client.csv", index=False)
    campaign.to_csv(output_folder / "campaign.csv", index=False)
    economics.to_csv(output_folder / "economics.csv", index=False)
    return


if __name__ == "__main__":
    clean_campaign_data()
