import pandas as pd
from pathlib import Path



def format_folder(folder_path: Path) -> None:
    """
    Formats all CSV files in a folder (recursively) to display floating point numbers with exactly 3 digits after decimal.

    Args:
        folder_path (Path): Path object of folder containing CSV files.
    
    Returns:
        None
    """

    for csv_file in folder_path.rglob("*.csv"):

        if "fmt" in csv_file.name:
            continue

        out_path = csv_file.with_name(f"{csv_file.stem}_fmt.csv")

        df = pd.read_csv(csv_file, na_filter=False)

        for col in df.columns:
            series = df[col]

            s_num = pd.to_numeric(series, errors="coerce")
            if s_num.isna().all():
                continue


            is_missing = (series == "") | (s_num.isna())

            non_missing_values = s_num[~is_missing]
            if (non_missing_values == non_missing_values.astype(int)).all():
                df[col] = pd.Series(
                    [int(v) if not missing else pd.NA
                     for v, missing in zip(s_num, is_missing)],
                    dtype="Int64"
                )

            else:
                df[col] = pd.Series(
                    [f"{float(v):.3f}" if not missing else pd.NA
                     for v, missing in zip(s_num, is_missing)],
                    dtype="object"
                )

        df.to_csv(out_path, index=False)



if __name__ == "__main__":
    format_folder(Path("results/"))