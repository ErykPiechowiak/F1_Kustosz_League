import pandas as pd
from database import RaceResult, get_session_direct

is_sprint = False

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

def main():
    race_data = pd.read_csv("race_results/event_182441_tier_1_results.csv")
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
            else:
                points_ = points_normal[record["Position"]] if record["Position"] in points_normal else 0
            result = RaceResult(
                player_name=record["PlayerName"],
                constructor_name=record["ConstructorName"],
                track_name=record["TrackName"],
                position=record["Position"],
                fastest_lap=record["FastestLap"],
                has_fastest_lap = record["HasFastestLap"],
                time = record["Time"],
                points = points_
            )
                
            session.add(result)
            session.commit()
            print("Dodano rekord")

if __name__ == "__main__":
    main()