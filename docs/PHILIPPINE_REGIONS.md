## Convention for REGION Value in Settings

To ensure consistency and machine-readability across the OpenBayanMesh-Edge ecosystem, the `REGION` environment variable (e.g., in `.env` files) should adhere to the following convention:

**Format:** `PH-REGIONABBREVIATION`

Where `PH` denotes the Philippines, and `REGIONABBREVIATION` is the official or commonly accepted abbreviation for the administrative region, as listed in this document. For regions without a standard abbreviation, a simplified, uppercase version of the region name or number should be used.

### Examples:

-   **National Capital Region:** `PH-NCR`
-   **Cordillera Administrative Region:** `PH-CAR`
-   **Ilocos Region:** `PH-REGION1` (or `PH-R1`)
-   **CALABARZON:** `PH-CALABARZON`
-   **MIMAROPA:** `PH-MIMAROPA`
-   **Davao Region:** `PH-REGION11` (or `PH-R11`)
-   **Bangsamoro Autonomous Region in Muslim Mindanao:** `PH-BARMM`

This convention allows for easy identification of the geographical deployment location of an OpenBayanMesh-Edge node and facilitates regional-specific configurations or data routing.

When setting the `REGION` variable, please refer to the abbreviations provided in the region list above to ensure compliance with this standard.