using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FantPlayer : MonoBehaviour{

    public int Passing { get; set; }
    public int Moving { get; set; }
    public int Shooting { get; set; }
    public int Combat { get; set; }
    public int Defence { get; set; }
    public int Actions { get; set; }
    public PlayerRace Race { get; set; }
    public Vector2Int Poss { get; set; }
    public bool HasBall { get; set; }
    private SpriteRenderer sr;


    //Inital Constructor
    public FantPlayer() { }
    
    //Constructor that fills in all properties
    public FantPlayer(int passing, int moving, int shooting, int combat, int defence, string tag, PlayerRace race)
    {
        Passing = passing;
        Moving = moving;
        Shooting = shooting;
        Combat = combat;
        Defence = defence;
        Race = race;
        this.tag = tag;
        HasBall = false;
    }

    public void Start()
    {
        if(transform.GetChild(0).GetComponent<SpriteRenderer>() != null)
        {
            sr = transform.GetChild(0).GetComponent<SpriteRenderer>();
        }
        else
        {
            sr = null;
        }
            
    }

    public void Update()
    {
        if (transform.GetChild(0).GetComponent<SpriteRenderer>() != null)
        {
            if (HasBall)
            {
                sr.enabled = true;
            }
            else
            {
                sr.enabled = false;
            }
        }
    }

    //allows to set the stats of the player easily
    public void SetStats(int passing, int moving, int shooting, int combat, int defence, PlayerRace race, Vector2Int poss)
    {
        Passing = passing;
        Moving = moving;
        Shooting = shooting;
        Combat = combat;
        Defence = defence;
        Race = race;
        Poss = poss;
    }

}
