import pandas as pd
from sqlalchemy import select, func
from database import RaceResult, get_session_direct, QualiResult
from pathlib import Path

is_sprint = False
SEASON = 1

def clean_trailing_commas(file_path: Path):
    lines = file_path.read_text().splitlines()

    cleaned = [
        line[:-1] if line.endswith(",") else line
        for line in lines
    ]

    file_path.write_text("\n".join(cleaned))

points_normal = {
    1 : 25,
    2 : 18,
    3 : 15,
    4 : 12,
    5 : 10,
    6 : 8,
    7 : 6,
    8 : 4,
    9 : 2,
    10 : 1
}

points_sprint = {
    1 : 8,
    2 : 7,
    3 : 6,
    4 : 5,
    5 : 4,
    6 : 3,
    7 : 2,
    8 : 1
}

def get_round_nr(file_name:str):
    #get lastest round nr from filename 
    tokens = file_name.split('_')
    return tokens[0] #round nr is first

def main():
    #race_data = pd.read_csv("race_results/event_182441_tier_1_results.csv")

    folder = Path("race_results")

    for file in folder.glob("*.csv"):
        if "qualifying" not in file.name:
            if file.name.endswith("_done.csv"):
                continue
            if "sprint" in file.name:
                is_sprint = True
            else:
                is_sprint = False

            print(f"Importing: {file.name}")

            try:
                clean_trailing_commas(file)

                race_data = pd.read_csv(file)
                for record in race_data.to_dict(orient="records"):
                    if pd.isna(list(record.values())).any():
                        print("NA: ",sep=" ")
                        print(record)
                        continue
                    print(record["PlayerName"])
                    with get_session_direct() as session:
                        points_ = 0
                        if is_sprint:
                            points_ = points_sprint[record["Position"]] if record["Position"] in points_sprint else 0
                            track_name_ = f"{record["TrackName"]}-sprint"
                        else:
                            points_ = points_normal[record["Position"]] if record["Position"] in points_normal else 0
                            track_name_ = f"{record["TrackName"]}"

                        result = RaceResult(
                            season = SEASON,
                            round_nr = get_round_nr(file.name),
                            player_name=record["PlayerName"],
                            constructor_name=record["ConstructorName"],
                            track_name = track_name_,
                            position=record["Position"],
                            fastest_lap=record["FastestLap"],
                            has_fastest_lap = record["HasFastestLap"],
                            time = record["Time"],
                            points = points_
                        )

                        session.add(result)
                        session.commit()
                        print("Added record")

                print(f"OK: {file.name}")

                done_file = file.with_name(file.stem + "_done.csv")
                file.rename(done_file)

            except Exception as e:
                print(f"error in {file.name}: {e}")
        else:
            if file.name.endswith("_done.csv"):
                continue
            if "sprint" in file.name:
                is_sprint = True
            else:
                is_sprint = False
            print(f"Importing: {file.name}")

            try:
                clean_trailing_commas(file)

                race_data = pd.read_csv(file)
                for record in race_data.to_dict(orient="records"):
                    if pd.isna(list(record.values())).any():
                        print("NA: ",sep=" ")
                        print(record)
                        continue
                    print(record["PlayerName"])
                    with get_session_direct() as session:
                        points_ = 0
                        if is_sprint:
                            track_name_ = f"{record["TrackName"]}-sprint"
                        else:
                            track_name_ = f"{record["TrackName"]}"

                        result = QualiResult(
                            season = SEASON,
                            round_nr = get_round_nr(file.name),
                            player_name=record["PlayerName"],
                            constructor_name=record["ConstructorName"],
                            track_name = track_name_,
                            quali_time=record["QualifyingTime"],
                        )

                        session.add(result)
                        session.commit()
                        print("Added record")

                print(f"OK: {file.name}")

                done_file = file.with_name(file.stem + "_done.csv")
                file.rename(done_file)

            except Exception as e:
                print(f"error in {file.name}: {e}")


if __name__ == "__main__":
    main()