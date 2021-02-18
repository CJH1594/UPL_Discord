import discord
import random
import os
from random import shuffle



class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('?UPL'):
             
            # A function that makes the match lsit with the members
            def match(N, Attendee):
                # To make the match list random, shuffle the members
                A = []
                for i in Attendee:
                    A.append(i)
                shuffle(A)
                
                matches = []
                
                if N % 2 == 1:
                    for v in range(N):
                        matches.append([])
                        A = A[1:] + A[0:1]
                        for u in range(N//2):
                            matches[-1].append([A[u+1],A[N-u-1]])
                
                else:
                    for v in range(N//2):
                        matches.append([])
                        A = A[1:] + A[0:1]
                        for u in range(N//2):
                            matches[-1].append([A[u],A[N-u-1]])
                        
                    for c in range(N//2 - 1):
                        matches.append([])
                        for u in range(N//2 - 1):
                            matches[-1].append([A[u],A[N-u-2]])
                        matches[-1].append([A[-1],A[N//2 - 1]])
                        A = A[len(A) - 1 : len(A)] + A[0 : len(A) - 1]
                return matches

            # A function that change the members to their team
            def Name_Team_Switcher(N, member, MatchList):
                matchTeam = []
                for i in range(len(MatchList)):
                    match_of_a_day = []
                    for v in range(N//2):
                        aMatch = []
                        for u in MatchList[i][v]:
                            aMatch.append(member[u])
                        match_of_a_day.append(aMatch)
                    matchTeam.append(match_of_a_day)
                return matchTeam
                
            # A function that makes ScoreBoard in descending order
            def sort(ScoreBoard):
                OrderedScoreBoard = {}
                val = list(set(ScoreBoard.values()))
                for v in range(len(val)):
                    for i in ScoreBoard:
                        if ScoreBoard[i] == max(val):
                            OrderedScoreBoard[i] = max(val)
                    val.remove(max(val))
                return OrderedScoreBoard

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()



            Attendee = []
            Team = []
            member = {}
            PointList = {}
            ScoreBoard = {}
            await message.channel.send("몇명이서 하냐? ")
            try:
                N = await self.wait_for('message', check=is_correct, timeout=10.0)
                N = int(N.content)
            except:
                await message.channel.send('잘좀 쓰자.')

            # A code that input the Teams
            for i in range(N):
                await message.channel.send('{}번째 이름이랑 팀이 뭐냐? ' .format(i+1))
                try:
                    X = await self.wait_for('message')
                    X = X.content.split()
                    Attendee.append(X[0])
                    Team.append(X[1])
                    member[X[0]] = X[1]
                    PointList[X[1]] = 0
                except:
                    await message.channel.send('잘좀 쓰자.')
                
            # Print mathList
            MatchList = match(N, Attendee)
            matchTeam = Name_Team_Switcher(N, member, MatchList)

            for i in range(len(MatchList)*3):
                await message.channel.send("이번 경기 매치업이다. ")
                for v in range(N//2):
                    await message.channel.send('{} - {}' .format(MatchList[i][v][0],MatchList[i][v][1]))
                await message.channel.send('이긴 팁을 입력해라. ')

                #승점 기록 part
                
                # Input all win team
                while True:
                    
                    WinTeam = []
                    TieTeam = []

                    # Print the Team rate and the Team
                    for u in range(len(Team)):
                        await message.channel.send('[{}] {}' .format(u+1, Team[u]))

                    WinTeamNumbers = await self.wait_for('message')
                    try:
                        WinTeamNumbers = WinTeamNumbers.content
                    except:
                        await message.channel.send('잘좀 쓰자.')
                        
                    try:
                        WinTeamNumbers = WinTeamNumbers.split()
                        WinTeamNumbers = list(map(int, WinTeamNumbers))
                    except:
                        if len(WinTeamNumbers) == 1:
                            WinTeamNumbers = [int(WinTeamNumbers)]
                        elif WinTeamNumbers == '':
                            WinTeamNumbers = []
                            
                    for u in WinTeamNumbers:
                        WinTeam.append(Team[u-1])
                    await message.channel.send(WinTeam)
                    await message.channel.send('확실 하냐? (ㅇ/ㄴ) ')
                    try:
                        D = await self.wait_for('message')
                        D = D.content
                    except:
                        await message.channel.send('잘좀 쓰자.')

                    if D == 'ㅇ' or D == 'd':
                        break
                    else:
                        await message.channel.send('잘좀 쓰자.')

                # Make the TieTeam as the matchTeam
                for u in matchTeam[i]:
                    TieTeam.append(u)

                # Add win point for the WinTeam
                for u in WinTeam:
                    PointList[u] += 3
                    
                    # Get rid of Win Team from TieTeam
                    for v in matchTeam[i]:
                        if u in v:
                            TieTeam.remove(v)

                # Listlize TieTeam
                TieTeam = sum(TieTeam,[])

                # Add win point for the TieTeam
                for i in TieTeam:
                    PointList[i] += 1
                
                PointList = sort(PointList)
                await message.channel.send('{}\n' .format(PointList))
                await message.channel.send('골을 기록해라.')

                while True:
                    t = 1
                    for i in ScoreBoard:
                        await message.channel.send('[{}] {} : {}' .format(t, i, ScoreBoard[i]))
                        t += 1

                    await message.channel.send('종료(0), 추가(1), 제거(2)')

                    try:
                        ScoreD = await self.wait_for('message')
                        ScoreD = int(ScoreD.content)
                    except:
                        await message.channel.send('잘 좀 쳐라.')

                    if ScoreD == 0:
                        await message.channel.send('종료할거냐? (ㅇ/ㄴ)')
                        try:
                            D = await self.wait_for('message')
                            D = D.content
                            if D == 'ㅇ' or D == 'd':
                                break
                        except:
                            await message.channel.send('잘좀 쓰자.')
                    elif ScoreD == 1:
                        await message.channel.send('골 누가 넣었냐? (뉴 페이스[0])')
                        try:
                            GoalGetterNumber = await self.wait_for('message')
                            GoalGetterNumber = int(GoalGetterNumber.content)
                        except:
                            await message.channel.send('잘 좀 쳐라.')

                        if GoalGetterNumber == 0:
                            await message.channel.send('선수 이름이 뭐냐?')
                            try:
                                GoalGetter = await self.wait_for('message')
                                GoalGetter = GoalGetter.content
                            except:
                                await message.channel.send('잘좀 쓰자.')

                            await message.channel.send('몇골 넣었냐?')
                            try:
                                GoalNumber = await self.wait_for('message')
                                GoalNumber = int(GoalNumber.content)
                                ScoreBoard[GoalGetter] = GoalNumber
                            except:
                                await message.channel.send('잘좀 쓰자.')

                        elif GoalGetterNumber in list(range(len(ScoreBoard)+1)):
                            GoalGetter = list(ScoreBoard.keys())[GoalGetterNumber-1]
                            await message.channel.send('몇골 넣었냐?')
                            try:
                                GoalNumber = await self.wait_for('message')
                                GoalNumber = int(GoalNumber.content)
                                ScoreBoard[GoalGetter] += GoalNumber
                            except:
                                await message.channel.send('잘 좀 쳐라')

                        else:
                            await message.channel.send('잘 좀 쳐라')

                        ScoreBoard = sort(ScoreBoard)

                    elif ScoreD == 2:
                        await message.channel.send('누구 지우게?')
                        try:
                            GoalGetterNumber = await self.wait_for('message')
                            GoalGetterNumber = int(GoalGetterNumber.content)
                            GoalGetter = list(ScoreBoard.keys())[GoalGetterNumber-1]
                            del ScoreBoard[GoalGetter]
                            ScoreBoard = sort(ScoreBoard)
                        except:
                            await message.channel.send('잘좀 쓰자.')
                    
                    else:
                        await message.channel.send('잘 좀 쳐라')

                        
                        
client = MyClient()
acess_token = os.environ['BOT_TOKEN']
client.run('acess_token')
