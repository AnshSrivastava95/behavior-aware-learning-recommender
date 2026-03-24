import pandas as pd

content_db=pd.read_csv("content.csv")
student_profile={
    "strategy":"focused",
    "prefered_modality":"practice",
    "prefered_difficulty":0.65
}

def recommend_focused(profile,df,unit,k=4):
    candidates=df[(df["unit"]==unit)&(df["modality"]==profile["prefered_modality"])].copy()
    candidates["score"]=1-abs(profile["prefered_difficulty"]-candidates["difficulty"])
    candidates=candidates.sort_values(by="score",ascending=False)
    return candidates.head(k)

def recommend_hybrid(profile, df, unit):

    candidates = df[df["unit"] == unit].copy()

    candidates["score"] = 1 - abs(
        profile["prefered_difficulty"] - candidates["difficulty"]
    )

    idx = candidates.groupby("modality")["score"].idxmax()

    return candidates.loc[idx]

def recommend(profile, df, unit):

    if profile["strategy"] == "focused":
        return recommend_focused(profile, df, unit)

    else:
        return recommend_hybrid(profile, df, unit)

result = recommend(student_profile, content_db, "memory_management")

print(result)