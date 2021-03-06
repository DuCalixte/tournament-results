#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered pla:yers appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testReportMatchesWithDraws():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, True)
    reportMatch(id3, id4, True)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id2, id3, id4) and playerDrawCount(i) != 1:
            raise ValueError("Each match player should have a draw recorded.")
        elif i in (id1, id2, id3, id4) and w != 0:
            raise ValueError("Each match player  should have zero wins recorded.")
    print "9. After a match with draws, players have updated standings."


def testReportMatchesWithPreventRematch():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)

    """These are the rematches that should not occur"""
    reportMatch(id2, id1)
    reportMatch(id4, id3)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "10. After preventing rematches, players have updated standings."


def testReportMatchesWithBuy():
    deleteMatches()
    deletePlayers()
    registerPlayer("John Woods")
    registerPlayer("Julia Sky")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1)
    reportMatch(id2)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id2) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
    print "11. After a bye match, players have updated standings."


def testReportMatchesWithNoBuyRematch():
    deleteMatches()
    deletePlayers()
    registerPlayer("John Woods")
    registerPlayer("Julia Sky")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    reportMatch(id1)
    reportMatch(id2)

    """ Attempt to give these players another bye win"""
    reportMatch(id1)
    reportMatch(id2)

    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id2) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
    print "12. After a bye match with rematch prevention, players have updated standings."



def testSortingWithOMW():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")

    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    
    """ Having Player plays 4 matches with wins"""
    reportMatch(id1, id2)
    reportMatch(id1, id3)
    reportMatch(id1, id4)

    reportMatch(id2, id4)
    reportMatch(id2)

    reportMatch(id4, id3)
    reportMatch(id3)

    standings = playerStandings()

    expected = [id1, id2, id4, id3]
    actual = [row[0] for row in standings]

    if expected != actual:
       raise ValueError("The sorting order did not show as exptected.")
    print "13. Verifying sortings, players have updated standings."


def testTournamentWithSwissPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")

    registerPlayer("John Woods")
    registerPlayer("Julia Sky")
    registerPlayer("Bruno Mars")
    registerPlayer("Alain De Lon")

    registerPlayer("John Muir")
    registerPlayer("Bob Marley")
    registerPlayer("Peter Jackson")
    registerPlayer("Michael Jackson")

    registerPlayer("Elizabeth Taylor")
    registerPlayer("Robert De Niro")
    registerPlayer("John Travolta")
    registerPlayer("Julia Roberts")

    registerPlayer("Cindy Kool")

    round=5
    for play  in range(0,round):
        pairings = swissPairings()
        [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8), (pid9, pname9, pid10, pname10), (pid11, pname11, pid12, pname12), (pid13, pname13, pid14, pname14), (pid15, pname15, pid16, pname16), (pid17, pname17)] = pairings
        reportMatch(pid1, pid2)
        reportMatch(pid3, pid4)
        reportMatch(pid5, pid6)
        reportMatch(pid7, pid8)
        reportMatch(pid9, pid10)
        reportMatch(pid11, pid12)
        reportMatch(pid13, pid14)
        reportMatch(pid15, pid16)
        reportMatch(pid17)


    standings = playerStandings()

    for (i, n, w, m) in standings:
        if m != 5:
            raise ValueError("Each player should have five  matches recorded.")

    print "14. Congratulations, we have a winner %s with %s wins" %(standings[0][1], standings[0][2])



if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testReportMatchesWithDraws()
    testReportMatchesWithPreventRematch()
    testReportMatchesWithBuy()
    testReportMatchesWithNoBuyRematch()
    testSortingWithOMW()
    testTournamentWithSwissPairings()
    print "Success!  All tests pass!"


