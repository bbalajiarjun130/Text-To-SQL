from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    full_prompt = f"{prompt[0]}\n{question}"
    response =  model.generate_content(full_prompt)
    return response.text.strip()

## Fucntion To retrieve query from the database

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if sql.strip().lower().startswith("select"):
            cur.execute(sql)
            rows = cur.fetchall()
        else:
            cur.executescript(sql)
            rows = [("No SELECT results to show.",)]

        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return [("An error occurred:", str(e))]
    
## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL queries.
    The database is called NBA.db and contains the following tables and common columns:

    1. common_player_info(person_id,first_name,last_name,display_first_last,display_last_comma_first,display_fi_last,player_slug,birthdate,school,country,last_affiliation,height,weight,season_exp,jersey,position,rosterstatus,games_played_current_season_flag,team_id,team_name,team_abbreviation,team_code,team_city,playercode,from_year,to_year,dleague_flag,nba_flag,games_played_flag,draft_year,draft_round,draft_number,greatest_75_flag)
    2. draft_combine_stats(season,player_id,first_name,last_name,player_name,position,height_wo_shoes,height_wo_shoes_ft_in,height_w_shoes,height_w_shoes_ft_in,weight,wingspan,wingspan_ft_in,standing_reach,standing_reach_ft_in,body_fat_pct,hand_length,hand_width,standing_vertical_leap,max_vertical_leap,lane_agility_time,modified_lane_agility_time,three_quarter_sprint,bench_press,spot_fifteen_corner_left,spot_fifteen_break_left,spot_fifteen_top_key,spot_fifteen_break_right,spot_fifteen_corner_right,spot_college_corner_left,spot_college_break_left,spot_college_top_key,spot_college_break_right,spot_college_corner_right,spot_nba_corner_left,spot_nba_break_left,spot_nba_top_key,spot_nba_break_right,spot_nba_corner_right,off_drib_fifteen_break_left,off_drib_fifteen_top_key,off_drib_fifteen_break_right,off_drib_college_break_left,off_drib_college_top_key,off_drib_college_break_right,on_move_fifteen,on_move_college)
    3. draft_history(person_id,player_name,season,round_number,round_pick,overall_pick,draft_type,team_id,team_city,team_name,team_abbreviation,organization,organization_type,player_profile_flag)
    4. game_info(game_id,game_date,attendance,game_time)
    5. game_summary(game_date_est,game_sequence,game_id,game_status_id,game_status_text,gamecode,home_team_id,visitor_team_id,season,live_period,live_pc_time,natl_tv_broadcaster_abbreviation,live_period_time_bcast,wh_status)
    6. game(season_id,team_id_home,team_abbreviation_home,team_name_home,game_id,game_date,matchup_home,wl_home,min,fgm_home,fga_home,fg_pct_home,fg3m_home,fg3a_home,fg3_pct_home,ftm_home,fta_home,ft_pct_home,oreb_home,dreb_home,reb_home,ast_home,stl_home,blk_home,tov_home,pf_home,pts_home,plus_minus_home,video_available_home,team_id_away,team_abbreviation_away,team_name_away,matchup_away,wl_away,fgm_away,fga_away,fg_pct_away,fg3m_away,fg3a_away,fg3_pct_away,ftm_away,fta_away,ft_pct_away,oreb_away,dreb_away,reb_away,ast_away,stl_away,blk_away,tov_away,pf_away,pts_away,plus_minus_away,video_available_away,season_type)
    7. inactive_players(game_id,player_id,first_name,last_name,jersey_num,team_id,team_city,team_name,team_abbreviation)
    8. line_score(game_date_est,game_sequence,game_id,team_id_home,team_abbreviation_home,team_city_name_home,team_nickname_home,team_wins_losses_home,pts_qtr1_home,pts_qtr2_home,pts_qtr3_home,pts_qtr4_home,pts_ot1_home,pts_ot2_home,pts_ot3_home,pts_ot4_home,pts_ot5_home,pts_ot6_home,pts_ot7_home,pts_ot8_home,pts_ot9_home,pts_ot10_home,pts_home,team_id_away,team_abbreviation_away,team_city_name_away,team_nickname_away,team_wins_losses_away,pts_qtr1_away,pts_qtr2_away,pts_qtr3_away,pts_qtr4_away,pts_ot1_away,pts_ot2_away,pts_ot3_away,pts_ot4_away,pts_ot5_away,pts_ot6_away,pts_ot7_away,pts_ot8_away,pts_ot9_away,pts_ot10_away,pts_away)
    9. officials(game_id,official_id,first_name,last_name,jersey_num)
    10. other_stats(game_id,league_id,team_id_home,team_abbreviation_home,team_city_home,pts_paint_home,pts_2nd_chance_home,pts_fb_home,largest_lead_home,lead_changes,times_tied,team_turnovers_home,total_turnovers_home,team_rebounds_home,pts_off_to_home,team_id_away,team_abbreviation_away,team_city_away,pts_paint_away,pts_2nd_chance_away,pts_fb_away,largest_lead_away,team_turnovers_away,total_turnovers_away,team_rebounds_away,pts_off_to_away)
    11. play_by_play(game_id,eventnum,eventmsgtype,eventmsgactiontype,period,wctimestring,pctimestring,homedescription,neutraldescription,visitordescription,score,scoremargin,person1type,player1_id,player1_name,player1_team_id,player1_team_city,player1_team_nickname,player1_team_abbreviation,person2type,player2_id,player2_name,player2_team_id,player2_team_city,player2_team_nickname,player2_team_abbreviation,person3type,player3_id,player3_name,player3_team_id,player3_team_city,player3_team_nickname,player3_team_abbreviation,video_available_flag)
    12. player(id,full_name,first_name,last_name,is_active)
    13. team_details(team_id,abbreviation,nickname,yearfounded,city,arena,arenacapacity,owner,generalmanager,headcoach,dleagueaffiliation,facebook,instagram,twitter)
    14. team_history(team_id,city,nickname,year_founded,year_active_till)
    15. team_info_common(team_id,season_year,team_city,team_name,team_abbreviation,team_conference,team_division,team_code,team_slug,w,l,pct,conf_rank,div_rank,min_year,max_year,league_id,season_id,pts_rank,pts_pg,reb_rank,reb_pg,ast_rank,ast_pg,opp_pts_rank,opp_pts_pg)
    16. team(id,full_name,abbreviation,nickname,city,state,year_founded)

    Here are some examples of how to convert questions to SQL queries:

    Question: 
    SQL Query: SELECT full_name FROM common_player_info WHERE person_id = 201939;

    Question: What is the team name of the team with team_id 1610612737?
    SQL Query: SELECT team_name FROM team WHERE id = 1610612737;

    Question: What is the average points per game for the team with team_id 1610612737 in the 2022 season?
    SQL Query: SELECT AVG(pts_pg) FROM team_info_common WHERE team_id = 1610612737 AND season_year = '2022';

     Only return valid SQL. Do not include markdown formatting or 'sql' tags. Do not include explanations — just the query.
    """


]

# Streamlit App UI
st.set_page_config(page_title="NBA Text-to-SQL with Gemini")
st.header("Ask the NBA Stats Assistant")

question = st.text_input("Ask a question about NBA stats:", key="input")
submit = st.button("Submit")

if submit and question:
    with st.spinner("Generating SQL and fetching results..."):
        sql_query = get_gemini_response(question, prompt)
        st.code(sql_query, language='sql')  # Show the generated query
        results = read_sql_query(sql_query, "NBA.db")
        st.subheader("Results:")
        for row in results:
            st.write(row)