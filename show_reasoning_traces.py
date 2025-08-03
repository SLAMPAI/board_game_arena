#!/usr/bin/env python3
"""
Demonstrate the enhanced reasoning traces with board states
"""

import sqlite3
import pandas as pd

def display_reasoning_traces():
    """Display the complete reasoning traces with board states"""

    print("🎮 Board Game Arena - Enhanced Reasoning Traces Demonstration")
    print("=" * 70)

    # Read from LLM database
    conn = sqlite3.connect('results/llm_litellm_groq_llama3_8b_8192.db')

    df = pd.read_sql_query("""
        SELECT game_name, episode, turn, action, reasoning,
               agent_type, agent_model, board_state, timestamp
        FROM moves
        ORDER BY game_name, episode, turn
    """, conn)

    conn.close()

    if len(df) == 0:
        print("❌ No reasoning traces found.")
        return

    print(f"✅ Found {len(df)} reasoning traces with complete information!")
    print()

    for i, row in df.iterrows():
        print(f"🧠 Reasoning Trace #{i+1}")
        print("-" * 40)
        print(f"🎯 Game: {row['game_name']}")
        print(f"📅 Episode: {row['episode']}, Turn: {row['turn']}")
        print(f"🤖 Agent: {row['agent_model']}")
        print(f"🎲 Action Chosen: {row['action']}")

        print(f"📋 Board State at Decision Time:")
        if row['board_state']:
            board_lines = row['board_state'].split('\n')
            for line in board_lines:
                print(f"     {line}")
        else:
            print("     [No board state recorded]")

        print(f"🧠 Agent's Reasoning:")
        if row['reasoning'] and row['reasoning'] != 'None':
            # Word wrap the reasoning for better display
            reasoning = row['reasoning']
            words = reasoning.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + " " + word) <= 60:
                    current_line += (" " + word if current_line else word)
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for line in lines:
                print(f"     {line}")
        else:
            print("     [No reasoning provided]")

        print(f"⏰ Timestamp: {row['timestamp']}")
        print()

    # Summary
    print("📊 Summary")
    print("-" * 20)
    print(f"✅ Board states captured: {(df['board_state'].notna() & (df['board_state'] != '')).sum()}/{len(df)}")
    print(f"✅ Reasoning captured: {(df['reasoning'].notna() & (df['reasoning'] != 'None') & (df['reasoning'] != '')).sum()}/{len(df)}")
    print(f"🎮 Games analyzed: {df['game_name'].nunique()}")
    print(f"📈 Episodes analyzed: {df['episode'].nunique()}")

    print()
    print("🎯 Key Achievement: Complete Reasoning Traces!")
    print("   - Board state at decision time ✅")
    print("   - Agent's reasoning process ✅")
    print("   - Action taken ✅")
    print("   - Full context and metadata ✅")
    print()
    print("💡 This enables deep analysis of LLM decision-making patterns!")

if __name__ == "__main__":
    display_reasoning_traces()
