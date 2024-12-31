import pandas as pd
import json
import os

# Function to process only ODI match data from the JSON and generate DataFrame
def create_odi_dataframe_from_json():
    folder_path = "extracted_odis_json"
    odi_match_data = []

    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        if isinstance(data, dict):
                            match_info = data.get('info', {})
                            teams = match_info.get("teams", [])
                            match_type = match_info.get("match_type", "Unknown")
                            match_date = match_info.get('dates', ["Unknown"])[0]
                            outcome = match_info.get('outcome')
                            winner = match_info.get('outcome', {}).get('winner', 'Unknown')
                            player_of_match = ", ".join(match_info.get("player_of_match", []))
                            
                            # Extract player statistics
                            player_stats = {}
                            for team in teams:
                                players = match_info.get("players", {}).get(team, [])
                                for player in players:
                                    player_stats[player] = {"runs": 0, "wickets": 0}
                            
                            innings_data = []
                            for innings in data.get("innings", []):
                                team = innings.get("team", "Unknown")
                                for over in innings.get("overs", []):
                                    over_number = over.get("over", "Unknown")
                                    for delivery in over.get("deliveries", []):
                                        batter = delivery.get("batter", "Unknown")
                                        bowler = delivery.get("bowler", "Unknown")
                                        runs_batter = delivery["runs"].get("batter", 0)
                                        extras_noballs = delivery["extras"].get("noballs", 0) if "extras" in delivery else 0
                                        runs_total = runs_batter + extras_noballs
                                        
                                        if batter in player_stats:
                                            player_stats[batter]["runs"] += runs_batter
                                        if bowler in player_stats:
                                            player_stats[bowler]["wickets"] += 1

                                        # Add row for each delivery
                                        odi_match_data.append({
                                            "match_date": match_date,
                                            "match_type": match_type,
                                            "teams": ", ".join(teams),
                                            "match_result": winner,
                                            "outcome":outcome,
                                            "player_of_match": player_of_match,
                                            "player": batter,
                                            "runs_batter": runs_batter,
                                            "wickets_bowler": player_stats[bowler]["wickets"],
                                            "extras_noballs": extras_noballs,
                                            "runs_total": runs_total,
                                            "over": over_number,
                                            "team": team
                                        })
                            
                            # Add player statistics to match data
                            for player, stats in player_stats.items():
                                odi_match_data.append({
                                    "match_date": match_date,
                                    "match_type": match_type,
                                    "teams": ", ".join(teams),
                                    "match_result": winner,
                                    "player_of_match": player_of_match,
                                    "outcome":outcome,
                                    "player": player,
                                    "runs_batter": stats["runs"],
                                    "wickets_bowler": stats["wickets"],
                                    "extras_noballs": 0,
                                    "runs_total": stats["runs"],
                                    "over": "N/A",
                                    "team": "All"
                                })
                        else:
                            print(f"Skipping invalid data format in file {filename}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from file {filename}")
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                print(f"Processed matches from {file_path}")
    else:
        print(f"Folder {folder_path} does not exist!")

    # Create DataFrame
    if odi_match_data:
        odi_matches_df = pd.DataFrame(odi_match_data)
        odi_matches_df.to_csv("odi_matches.csv", index=False)
        print("ODI DataFrame created and saved as odi_matches.csv.")
    else:
        print("No valid ODI match data found!")

# Example usage
if __name__ == "__main__":
    create_odi_dataframe_from_json()
