using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class Testgamemanager : MonoBehaviour
{

    [SerializeField]
    private List<PlayerType> teamComp = new List<PlayerType>();
    private GameObject[,] gridTile;
    private FantPlayer[,] gridPlayer;
    private GameObject[,] gridTileMod;

    [Header("Varibles")]
    [SerializeField]
    private int gridSizeX;

    [SerializeField]
    private int gridSizeY;
    private Vector2 mouseOver;
    private Vector2 previousTilePos = new Vector2(-1, -1);

    [SerializeField]
    private float animSpeed;

    [SerializeField]
    private Vector3 endShootPositionHuman;
    [SerializeField]
    private Vector3 endShootPositionOrc;
    private Vector3 startShootPosition;
    private Vector2 endShootScale;
    private Vector2 startShootScale;
    [SerializeField]
    private float animaionSpeed;
    private Vector3[] arcArray;
    private int arcArrayIndex;
    private bool advanceBall;
    private bool shootingBall;

    [SerializeField]
    private PlayerRace teamRace;

    private FantPlayer passingPlayer;
    private FantPlayer selectedPlayer;
    private bool canAct = false;
    private bool doActionOnce = true;

    private int humanScore = 0;
    private int orkScore = 0;

    public Sprite tileSelector;
    [Header("Player Base Stats")]
    public int baseMoveSpeed;
    public int baseAttackDamage;

    private FantPlayer attackingPlayer;

    public bool actionMove = false;
    public bool actionAttack = false;
    public bool actionPass = false;
    public bool actionShoot = false;
    public bool drawnOnMap = false;

    #region GameObject Refrences
    [Header("PreFabs")]
    public GameObject tile;
    public GameObject tileGreen;
    public GameObject tileRed;
    public GameObject playerPazzer;
    public GameObject playerPassGaurd;
    public GameObject playerShootzer;
    public GameObject playerScoringGuard;
    public GameObject playerSmallDunker;
    public GameObject playerTallForward;
    public GameObject playerBuffOrc;
    public GameObject playerHulkForward;
    public GameObject playerBigBoi;
    public GameObject playerSmallTitan;

    [Header("GameObjects")]
    public GameObject fullActionCover;
    public GameObject partialActionCover;
    public GameObject goalHuman;
    public GameObject goalOrc;
    public GameObject backgroundCutscene;
    public GameObject basketBall;
    #endregion
    #region Text Refrences
    [Header("Text Refrences")]
    public TextMeshProUGUI actionText;
    public TextMeshProUGUI raceText;
    public TextMeshProUGUI classText;
    public TextMeshProUGUI passingText;
    public TextMeshProUGUI movingText;
    public TextMeshProUGUI shootingText;
    public TextMeshProUGUI combatText;
    public TextMeshProUGUI defenseText;
    public TextMeshProUGUI humanScoreText;
    public TextMeshProUGUI orkScoreText;
    #endregion

    void Start()
    {
        gridPlayer = new FantPlayer[gridSizeX, gridSizeY];
        gridTile = new GameObject[gridSizeX, gridSizeY];
        GenerateGrid(gridSizeX, gridSizeY);
        gridTileMod = new GameObject[gridSizeX, gridSizeY];
        SetUpBoard(teamComp);

        //DEBUG PURPOSES ONLY
        teamRace = PlayerRace.Human;
        gridPlayer[0, 0].HasBall = true;
        //DEBUG PURPOSES ONLY

    }
    void Update()
    {
        UpdateMouseOver();
        UpdateScore();


        // If it is my turn.
        {
            int x = (int)mouseOver.x;
            int y = (int)mouseOver.y;

            HighlightTile(x, y);

            if (Input.GetMouseButtonDown(0))
                SelectPiece(x, y);

            if (canAct)
            {
                OpenAction();
            }
        }

        if (shootingBall)
        {
            if (advanceBall && arcArray.Length >= arcArrayIndex)
            {
                StartCoroutine(LaunchBall());
                advanceBall = false;
                if (arcArray.Length < arcArrayIndex)
                {
                    shootingBall = false;
                }
            }
        }
    }
    // Really nasty way of doing this maybe... it works though
    private void HighlightTile(int x, int y)
    {
        if (x != -1 && y != -1)
        {
            SpriteRenderer sr = gridTile[x, y].GetComponent<SpriteRenderer>();
            for (int xl = 0; xl < gridTile.GetLength(0); xl++)
            {
                for (int yl = 0; yl < gridTile.GetLength(1); yl++)
                {
                    if (gridTile[xl, yl] == gridTile[x, y])
                    {
                        sr.sprite = tileSelector;
                    }
                    else
                    {
                        gridTile[xl, yl].GetComponent<SpriteRenderer>().sprite = tile.GetComponent<SpriteRenderer>().sprite;
                    }
                }
            }
        }
    }

    // Deals with action  bar and then waits for action to be selected, then do action.
    private void OpenAction()
    {
        if (selectedPlayer == null)
        {
            CoverActionsBar(0);
        }

        if (actionMove)
        {
            if (doActionOnce)
            {
                SeeMove(selectedPlayer.Poss.x, selectedPlayer.Poss.y);
                doActionOnce = false;
            }

            if (Input.GetMouseButtonUp(1))
            {
                DoMove();
                doActionOnce = true;
            }
        }

        if (actionAttack)
        {
            if (doActionOnce)
            {
                SeeAttack(selectedPlayer.Poss.x, selectedPlayer.Poss.y);
                doActionOnce = false;
            }

            if (Input.GetMouseButtonUp(1))
            {
                DoAttack();
                doActionOnce = true;
            }
        }
        if (actionPass)
        {
            if (actionPass)
            {
                if (doActionOnce)
                {
                    SeePass(selectedPlayer.Poss.x, selectedPlayer.Poss.y);
                    doActionOnce = false;
                }

                if (Input.GetMouseButtonUp(1))
                {
                    DoPass();
                    doActionOnce = true;
                }
            }
        }
        if (actionShoot)
        {
            if (doActionOnce)
            {
                SeeShoot(selectedPlayer.Poss.x, selectedPlayer.Poss.y);
                doActionOnce = false;
            }

            if (Input.GetMouseButtonUp(1))
            {
                DoShoot();
                doActionOnce = true;
            }
        }

    }

    // When you select a peice it will go though to logic to figure out if its on your team, if the player can move etc.
    private void SelectPiece(int x, int y)
    {
        //out of bounds
        if (x < 0 || x >= gridPlayer.GetLength(0) || y < 0 || y >= gridPlayer.GetLength(1))
            return;

        //gets access to the player
        FantPlayer fp = gridPlayer[x, y];
        if (fp != null)
        {
            selectedPlayer = fp;
            DeleteTileMods();
            Debug.Log(selectedPlayer.name);
            ShowPlayerStats(selectedPlayer);
            if (IsOnTeam(selectedPlayer))
            {
                if (selectedPlayer.Actions < 2)
                {
                    selectedPlayer.Poss = new Vector2Int(x, y);
                    canAct = true;
                    if (selectedPlayer.HasBall)
                    {
                        CoverActionsBar(2);
                    }
                    else
                    {
                        CoverActionsBar(1);
                    }

                }
            }
            else
            {
                CoverActionsBar(0);
            }

        }
    }

    // Shows the possible move that the player could make.
    private void SeeMove(int playerX, int playerY)
    {
        List<Vector2> moveablePos = new List<Vector2>();
        int moveDistance = selectedPlayer.Moving + baseMoveSpeed;

        if (selectedPlayer.HasBall)
        {
            moveDistance = selectedPlayer.Moving + (baseMoveSpeed / 2);
        }
        else
        {
            moveDistance = selectedPlayer.Moving + baseMoveSpeed;
        }

        // If tile mods have already been drawn it deletes it.
        if (drawnOnMap)
        {
            foreach (GameObject item in gridTileMod)
            {
                Destroy(item);
            }
        }
        else
        {
            drawnOnMap = true;
        }

        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (playerX + moveDistance > x && playerY + moveDistance > y && playerX - moveDistance < x && playerY - moveDistance < y)
                {
                    if (gridPlayer[x, y] == null)
                    {
                        moveablePos.Add(new Vector2(x, y));
                        gridTileMod[x, y] = Instantiate(tileGreen, new Vector3(OffSetX(x), OffSetY(y), -.5f), Quaternion.identity);
                        gridTileMod[x, y].name = "Green Tile (" + x + ", " + y + ")";
                    }
                }
                else
                {
                    // Don't think I need this.
                    //gridTileMod[x, y] = Instantiate(tile, new Vector3(offSetX(x), offSetY(y), -.5f), Quaternion.identity);
                }
            }
        }
    }

    // Checks if the player can move and moves him.
    private void DoMove()
    {
        if (selectedPlayer.Actions > 2)
            return;
        Vector2 newPos = (Camera.main.ScreenToWorldPoint(Input.mousePosition));
        newPos.x = (int)(newPos.x / 5);
        newPos.y = (int)((newPos.y - 15) / 5);

        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (gridTileMod[x, y] != null)
                {
                    if (x == newPos.x && y == newPos.y)
                    {
                        gridPlayer[selectedPlayer.Poss.x, selectedPlayer.Poss.y] = null;
                        gridPlayer[x, y] = selectedPlayer;

                        // Destroys all of the tile mods.
                        DeleteTileMods();

                        // Debug purpose.
                        MovePlayerDirect((int)newPos.x, (int)newPos.y, selectedPlayer);
                        selectedPlayer.Actions += 1;
                        CoverActionsBar(0);
                        actionMove = false;
                        ShowPlayerStats(selectedPlayer);
                    }
                }
            }
        }
    }

    // Shows the possible attacks the players can make.
    private void SeeAttack(int playerX, int playerY)
    {
        FantPlayer fp = gridPlayer[playerX, playerY];
        int attackDistance = 2;
        List<Vector2> attackRadius = new List<Vector2>();
        PlayerRace playerTeam = selectedPlayer.Race;

        // If tile mods have already been drawn it deletes it.
        if (drawnOnMap)
        {
            DeleteTileMods();
        }
        else
        {
            drawnOnMap = true;
        }

        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (gridPlayer[x, y] != null)
                {
                    if (gridPlayer[x, y].Race != playerTeam)
                    {
                        if (playerX + attackDistance > x && playerY + attackDistance > y && playerX - attackDistance < x && playerY - attackDistance < y)
                        {
                            attackRadius.Add(new Vector2(x, y));
                            gridTileMod[x, y] = Instantiate(tileRed, new Vector3(OffSetX(x), OffSetY(y), -.5f), Quaternion.identity);
                            gridTileMod[x, y].name = "Red Tile (" + x + ", " + y + ")";
                        }
                    }
                }

            }
        }
    }

    private void DoAttack()
    {
        if (selectedPlayer.Actions > 2)
            return;

        int attackingPlayer = selectedPlayer.Combat;

        Vector2 enemyPos = (Camera.main.ScreenToWorldPoint(Input.mousePosition));
        enemyPos.x = (int)(enemyPos.x / 5);
        enemyPos.y = (int)((enemyPos.y - 15) / 5);
        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (gridTileMod[x, y] != null)
                {
                    if (x == enemyPos.x && y == enemyPos.y)
                    {

                        gridPlayer[selectedPlayer.Poss.x, selectedPlayer.Poss.y] = null;
                        gridPlayer[x, y] = selectedPlayer;


                        DeleteTileMods();

                        int attackRoll = Random.Range(0, 101); //Decides what the combat role is

                        int modifier = attackingPlayer - selectedPlayer.Defence;

                        switch (modifier)
                        {
                            case 2:
                                if (attackRoll >= 0 && attackRoll <= 15)
                                {
                                    //MissGraze();
                                }
                                if (attackRoll >= 16 && attackRoll <= 89)
                                {
                                    KnockBack();
                                }
                                if (attackRoll >= 90 && attackRoll <= 100)
                                {
                                    KnockOut();
                                }
                                break;
                            case 1:
                                if (attackRoll >= 0 && attackRoll <= 25)
                                {
                                    //MissGraze();
                                }
                                if (attackRoll >= 26 && attackRoll <= 95)
                                {
                                    KnockBack();
                                }
                                if (attackRoll >= 90 && attackRoll <= 100)
                                {
                                    KnockOut();
                                }
                                break;
                            case 0:
                                if (attackRoll >= 0 && attackRoll <= 30)
                                {
                                    //MissGraze();
                                }
                                if (attackRoll >= 31 && attackRoll <= 98)
                                {
                                    KnockBack();
                                }
                                if (attackRoll >= 99 && attackRoll <= 100)
                                {
                                    KnockOut();
                                }
                                break;
                            case -1:
                                if (attackRoll >= 0 && attackRoll <= 35)
                                {
                                    //MissGraze();
                                }
                                if (attackRoll >= 36 && attackRoll <= 99)
                                {
                                    KnockBack();
                                }
                                if (attackRoll >= 100)
                                {
                                    KnockOut();
                                }
                                break;
                            case -2:
                                if (attackRoll >= 0 && attackRoll <= 69)
                                {
                                    //MissGraze();
                                }
                                if (attackRoll >= 70 && attackRoll <= 100)
                                {
                                    KnockBack();
                                }
                                break;
                        }

                        selectedPlayer.Actions += 1;
                        CoverActionsBar(0);
                        actionAttack = false;
                        ShowPlayerStats(selectedPlayer);

                    }
                }
            }
        }
    }

    private void SeePass(int playerX, int playerY)
    {
        FantPlayer fp = gridPlayer[playerX, playerY];
        int passDistance = selectedPlayer.Passing + 7;
        List<Vector2> passRadius = new List<Vector2>();
        PlayerRace playerTeam = selectedPlayer.Race;

        // If tile mods have already been drawn it deletes it.
        if (drawnOnMap)
        {
            DeleteTileMods();
        }
        else
        {
            drawnOnMap = true;
        }

        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (gridPlayer[x, y] != null)
                {
                    if (gridPlayer[x, y].Race == playerTeam)
                    {
                        if (playerX + passDistance > x && playerY + passDistance > y && playerX - passDistance < x && playerY - passDistance < y)
                        {
                            passRadius.Add(new Vector2(x, y));
                            gridTileMod[x, y] = Instantiate(tileGreen, new Vector3(OffSetX(x), OffSetY(y), -.5f), Quaternion.identity);
                            gridTileMod[x, y].name = "Green Tile (" + x + ", " + y + ")";
                        }
                    }
                }

            }
        }
    }

    private void DoPass()
    {
        if (selectedPlayer.Actions > 2)
            return;

        passingPlayer = selectedPlayer;

        Vector2 passPoss = (Camera.main.ScreenToWorldPoint(Input.mousePosition));
        passPoss.x = (int)(passPoss.x / 5);
        passPoss.y = (int)((passPoss.y - 15) / 5);
        for (int x = 0; x < gridTile.GetLength(0); x++)
        {
            for (int y = 0; y < gridTile.GetLength(1); y++)
            {
                if (gridTileMod[x, y] != null)
                {
                    if (x == passPoss.x && y == passPoss.y)
                    {

                        gridPlayer[selectedPlayer.Poss.x, selectedPlayer.Poss.y] = null;
                        gridPlayer[x, y] = selectedPlayer;


                        DeleteTileMods();


                        passingPlayer.HasBall = false;
                        selectedPlayer.HasBall = true;

                        passingPlayer.Actions -= 1;
                        CoverActionsBar(0);
                        actionAttack = false;
                        ShowPlayerStats(selectedPlayer);

                    }
                }
            }
        }
    }

    public void DoShoot()
    {
        // Set arc angel and velocity
        arcArray = LaunchArcRender.arcArray;

        // Shoots ball.
        shootingBall = true;
    }

    private void SeeShoot(int playerX, int playerY)
    {
        Vector3 startGoalPosition;
        arcArrayIndex = 0;
        startShootPosition = selectedPlayer.transform.position;
        backgroundCutscene.SetActive(true);
        advanceBall = true;

        #region Hide Players / Tiles
        foreach (FantPlayer fp in gridPlayer)
        {
            if (fp != null)
            {
                fp.gameObject.SetActive(false);
            }
        }

        for (int x = 0; x < 19; x++)
        {
            for (int y = 0; y < 4; y++)
            {
                gridTile[x, y].SetActive(false);
            }
        }
        #endregion

        // Finds which goal to be shooting on.
        if (selectedPlayer.Race == PlayerRace.Human)
        {
            // Grows and relocates player to left side of board.
            selectedPlayer.transform.localScale = new Vector2(selectedPlayer.transform.localScale.x * 3, selectedPlayer.transform.localScale.y * 3);
            selectedPlayer.transform.position = endShootPositionHuman;
            selectedPlayer.gameObject.SetActive(true);
            // Grows and relocates goal to right side of board.
            startGoalPosition = goalHuman.transform.position;
            goalHuman.transform.position = endShootPositionOrc;
            goalHuman.transform.localScale = new Vector2(goalHuman.transform.localScale.x * 3, goalHuman.transform.localScale.y * 3);
            goalOrc.SetActive(false);
            // Sets up the launch arcs inital position.
            LaunchArcRender.startArcPosition = new Vector3(30.5f, 37, -10);


        }
        else
        {
            // Grows and relocates player to the right side.
            selectedPlayer.transform.localScale = new Vector2(selectedPlayer.transform.localScale.x * 3, selectedPlayer.transform.localScale.y * 3);
            selectedPlayer.transform.position = endShootPositionOrc;
            // Grows and relocates goal to the left side of board.
            startGoalPosition = goalOrc.transform.position;
            goalOrc.transform.position = endShootPositionHuman;
            goalOrc.transform.localScale = new Vector2(goalOrc.transform.localScale.x * 3, goalOrc.transform.localScale.y * 3);
        }
    }

    private void SimulateRiemannSums()
    {

    }

    public void StopShoot()
    {

    }

    private IEnumerator LaunchBall()
    {
        yield return new WaitForSeconds(.125f);
        basketBall.transform.position = arcArray[arcArrayIndex];
        arcArrayIndex += 1;
        Debug.Log("Tick");
        advanceBall = true;
    }

    // Toggles if the action wanted is action move.
    public void ActionMove()
    {
        actionMove = !actionMove;
    }

    // Toggles if the action watned is to attack.
    public void ActionAttack()
    {
        actionAttack = !actionAttack;
    }

    // Toggles if the action watned is to Pass.
    public void ActionPass()
    {
        actionPass = !actionPass;
    }

    // Toggles if the action watned is to Shoot.
    public void ActionShoot()
    {
        actionShoot = !actionShoot;
    }

    // Disable the enemy player for one turn.
    void KnockOut()
    {
        Debug.Log("Knocked Out");
    }

    // Knock back the enemy player one tile.
    void KnockBack()
    {
        int pushBackPosition = 8;
        switch (pushBackPosition)
        {
            case 1:
                if (attackingPlayer.Poss.x > selectedPlayer.Poss.x)
                {
                    //Push back left 
                    MovePlayerDirect(selectedPlayer.Poss.x - 1, selectedPlayer.Poss.y, selectedPlayer);
                }
                break;
            case 2:
                if (attackingPlayer.Poss.x > selectedPlayer.Poss.x && attackingPlayer.Poss.y < selectedPlayer.Poss.y)
                {
                    //Push Up left
                    MovePlayerDirect(selectedPlayer.Poss.x - 1, selectedPlayer.Poss.y + 1, selectedPlayer);
                }
                break;
            case 3:
                if (attackingPlayer.Poss.y < selectedPlayer.Poss.y)
                {
                    //Push Up
                    MovePlayerDirect(selectedPlayer.Poss.x, selectedPlayer.Poss.y + 1, selectedPlayer);
                }
                break;
            case 4:
                if (attackingPlayer.Poss.x < selectedPlayer.Poss.x && attackingPlayer.Poss.y < selectedPlayer.Poss.y)
                {
                    //Push Up right
                    MovePlayerDirect(selectedPlayer.Poss.x + 1, selectedPlayer.Poss.y + 1, selectedPlayer);
                }
                break;
            case 5:
                if (attackingPlayer.Poss.x < selectedPlayer.Poss.x)
                {
                    //Push right
                    MovePlayerDirect(selectedPlayer.Poss.x + 1, selectedPlayer.Poss.y, selectedPlayer);
                }
                break;
            case 6:
                if (attackingPlayer.Poss.x < selectedPlayer.Poss.x && attackingPlayer.Poss.y > selectedPlayer.Poss.y)
                {
                    //Push down right
                    MovePlayerDirect(selectedPlayer.Poss.x + 1, selectedPlayer.Poss.y - 1, selectedPlayer);
                }
                break;
            case 7:
                if (attackingPlayer.Poss.y > selectedPlayer.Poss.y)
                {
                    //Push down
                    MovePlayerDirect(selectedPlayer.Poss.x, selectedPlayer.Poss.y - 1, selectedPlayer);
                }
                break;
            case 8:
                if (attackingPlayer.Poss.x > selectedPlayer.Poss.x && attackingPlayer.Poss.y > selectedPlayer.Poss.y)
                {
                    //Push down left
                    MovePlayerDirect(selectedPlayer.Poss.x - 1, selectedPlayer.Poss.y - 1, selectedPlayer);
                }
                break;
        }
    }

    // Checks if a player is on the clients team.
    private bool IsOnTeam(FantPlayer player)
    {
        return player.Race == teamRace;
    }

    // Plugs all of the players stats into fields.
    private void ShowPlayerStats(FantPlayer player)
    {
        actionText.text = ("Action: " + player.Actions.ToString());
        raceText.text = ("Race: " + player.Race.ToString());
        classText.text = ("Class: " + player.tag);
        passingText.text = ("Passing: " + player.Passing);
        movingText.text = ("Moving: " + player.Moving);
        shootingText.text = ("Shooting: " + player.Shooting);
        combatText.text = ("Combat: " + player.Combat);
        defenseText.text = ("Defese: " + player.Defence);
    }

    // Finds what grid space the mouse is currently in.
    private void UpdateMouseOver()
    {
        if (!Camera.main)
        {
            Debug.Log("Unable to find main Camera.");
            return;
        }

        RaycastHit hit;

        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out hit, 100.0f, LayerMask.GetMask("Board")))
        {
            mouseOver.x = (int)(hit.point.x / 5);
            mouseOver.y = (int)(hit.point.y / 5) - 3;
        }
        else
        {
            mouseOver.x = -1;
            mouseOver.y = -1;
        }
    }

    // Not sure if I like how this is done, but for now this is how the grid is placed.
    private void GenerateGrid(int sizeX, int sizeY)
    {
        for (int x = 0; x < sizeX; x++)
        {
            for (int y = 0; y < sizeY; y++)
            {

                gridTile[x, y] = Instantiate(tile, new Vector2(OffSetX(x), OffSetY(y)), Quaternion.identity, transform.GetChild(0));
                gridTile[x, y].name = "Tile (" + x + "," + y + ")";

            }
        }
    }

    // Sets up the board as soon as the game is started.
    private void SetUpBoard(List<PlayerType> teamComp)
    {
        //Generates left team
        for (int y = 0; y < teamComp.Count; y++)
        {
            //Generates a Player
            GeneratePlayer(0, y, teamComp[y], PlayerRace.Human);
        }

        //generates the right team
        for (int y = 0; y < teamComp.Count; y++)
        {
            //Generates a Player
            GeneratePlayer(18, y, teamComp[y], PlayerRace.Orc);
        }

        //Turns off action bar
        CoverActionsBar(0);

    }

    // Generates a player at an x and y position and is given a type.
    private void GeneratePlayer(int x, int y, PlayerType type, PlayerRace race)
    {
        GameObject go = null;
        int startingPassing = 0;
        int startingMoving = 0;
        int startingShooting = 0;
        int startingCombat = 0;
        int startingDefence = 0;

        #region Switch: Race & Type W/ Benefits

        switch (race)
        {
            case PlayerRace.Human:
                switch (type)
                {
                    case PlayerType.PointGuard:
                        go = Instantiate(playerPassGaurd);
                        startingCombat = -1;
                        startingDefence = 0;
                        startingMoving = 1;
                        startingPassing = 2;
                        startingShooting = 0;
                        break;
                    case PlayerType.ShootingGuard:
                        go = Instantiate(playerScoringGuard);
                        startingCombat = 0;
                        startingDefence = -1;
                        startingMoving = 0;
                        startingPassing = 1;
                        startingShooting = 2;
                        break;
                    case PlayerType.SmallForward:
                        go = Instantiate(playerTallForward);
                        startingCombat = 1;
                        startingDefence = 0;
                        startingMoving = 2;
                        startingPassing = 0;
                        startingShooting = -1;
                        break;
                    case PlayerType.PowerForward:
                        go = Instantiate(playerHulkForward);
                        startingCombat = 1;
                        startingDefence = 2;
                        startingMoving = 0;
                        startingPassing = 0;
                        startingShooting = -1;
                        break;
                    case PlayerType.Center:
                        go = Instantiate(playerSmallTitan);
                        startingCombat = 2;
                        startingDefence = 2;
                        startingMoving = -2;
                        startingPassing = 0;
                        startingShooting = -2;
                        break;
                    default:
                        Debug.LogError("Human instaniate error");
                        break;
                }
                break;
            case PlayerRace.Orc:
                switch (type)
                {
                    case PlayerType.PointGuard:
                        go = Instantiate(playerPazzer);
                        startingCombat = -1;
                        startingDefence = 0;
                        startingMoving = 1;
                        startingPassing = 2;
                        startingShooting = 0;
                        break;
                    case PlayerType.ShootingGuard:
                        go = Instantiate(playerShootzer);
                        startingCombat = 0;
                        startingDefence = -1;
                        startingMoving = 0;
                        startingPassing = 1;
                        startingShooting = 2;
                        break;
                    case PlayerType.SmallForward:
                        go = Instantiate(playerSmallDunker);
                        startingCombat = 1;
                        startingDefence = 0;
                        startingMoving = 2;
                        startingPassing = 0;
                        startingShooting = -1;
                        break;
                    case PlayerType.PowerForward:
                        go = Instantiate(playerBuffOrc);
                        startingCombat = 1;
                        startingDefence = 2;
                        startingMoving = 0;
                        startingPassing = 0;
                        startingShooting = -1;
                        break;
                    case PlayerType.Center:
                        go = Instantiate(playerBigBoi);
                        startingCombat = 2;
                        startingDefence = 2;
                        startingMoving = -2;
                        startingPassing = 0;
                        startingShooting = -2;
                        break;
                    default:
                        Debug.LogError("Orc instaniate error");
                        break;
                }
                break;
            default:
                Debug.LogError("Instaniate player error");
                break;
        }
        #endregion

        FantPlayer fp = go.GetComponent<FantPlayer>();
        MovePlayerDirect(x, y, fp);
        fp.SetStats(startingPassing, startingMoving, startingShooting, startingCombat, startingDefence, race, new Vector2Int(x, y));
        go.transform.SetParent(transform.GetChild(1));
        go.tag = type.ToString();
        go.name = (race.ToString() + ": " + type.ToString());
        gridPlayer[x, y] = fp;
    }

    // Contains the diffrent ways to move players.
    #region Move Player Methods

    // Moves a player to a x,y location.
    private void MovePlayerDirect(int x, int y, FantPlayer fp)
    {
        fp.transform.position = new Vector3(OffSetX(x), OffSetY(y) + 3f, -1);
        SpriteRenderer sr = fp.GetComponent<SpriteRenderer>();
        sr.sortingOrder = -y;
    }

    // Moves a player to a position tile to tile with pathing around people.
    private void MovePlayer(int x, int y, FantPlayer fp)
    {
        Vector2Int currentPos = new Vector2Int(fp.Poss.x, fp.Poss.y);
        Vector2Int targetPos = new Vector2Int(x, y);
        Direction moveDirection;

        #region Find Direction
        if (currentPos.x > targetPos.x)
        {
            if (currentPos.y > targetPos.y)
            {
                moveDirection = Direction.DownLeft;
            }
            else
            {
                moveDirection = Direction.UpLeft;
            }
        }
        else
        {
            if (currentPos.y > targetPos.y)
            {
                moveDirection = Direction.DownRight;
            }
            else
            {
                moveDirection = Direction.UpRight;
            }
        }
        #endregion

        switch (moveDirection)
        {
            case Direction.UpRight:
                while (currentPos != targetPos)
                {
                    if (gridPlayer[currentPos.x + 1, currentPos.y] == null)
                    {
                        fp.transform.position = new Vector2(OffSetX(currentPos.x + 1), OffSetY(currentPos.y));
                    }
                    else
                    {
                        if (gridPlayer[currentPos.x, currentPos.y + 1] == null)
                        {
                            fp.transform.position = new Vector2(OffSetX(currentPos.x), OffSetY(currentPos.y + 1));
                        }
                    }
                }
                break;
            case Direction.UpLeft:
                break;
            case Direction.DownRight:
                break;
            case Direction.DownLeft:
                break;
            default:
                break;
        }


    }
    #endregion

    //Offsets for the board
    #region Offsets
    // Offset for the x axis on the grid.
    private float OffSetX(int x)
    {
        return ((x * 5) + 2.5f);
    }

    // Offset for the y axit on the grid.
    private float OffSetY(int y)
    {
        return ((y * 5) + 17);
    }
    #endregion

    // Toggles the action bar cover 0 - full 1 - patial 2 - none.
    private void CoverActionsBar(int fullCover)
    {
        Image imageFull = fullActionCover.GetComponent<Image>();
        Image imagePartial = partialActionCover.GetComponent<Image>();

        if (fullCover == 0)
        {
            imageFull.enabled = true;
            imagePartial.enabled = false;
        }
        else
        {
            if (fullCover == 1)
            {
                imageFull.enabled = false;
                imagePartial.enabled = true;
            }
            else
            {
                imageFull.enabled = false;
                imagePartial.enabled = false;
            }
        }
    }

    // Destroys all of the tile mods.
    private void DeleteTileMods()
    {
        foreach (GameObject item in gridTileMod)
        {
            Destroy(item);
        }

        actionPass = false;
        actionMove = false;
        actionShoot = false;
        actionAttack = false;
        drawnOnMap = false;
    }

    private void UpdateScore()
    {
        orkScoreText.text = orkScore.ToString();
        humanScoreText.text = humanScore.ToString();
    }

    /*
    private void StartShootAnimation()
    {
        Vector2 initalPosition = selectedPlayer.transform.position;
        Vector2 currentPosition = initalPosition;
        bool isOnX = false;
        bool isOnY = false;


        while(!isOnX && !isOnY)
        {
            if (selectedPlayer.transform.position.x != endShootPosition.x)
            {
                currentPosition.x += animaionSpeed;
            }
            else
            {
                isOnX = true;
            }

            if (selectedPlayer.transform.position.y != endShootPosition.y)
            {
                currentPosition.y += animaionSpeed;
            }
            else
            {
                isOnY = false;
            }

            selectedPlayer.transform.position = currentPosition;
        }
      
    }
    */
}
