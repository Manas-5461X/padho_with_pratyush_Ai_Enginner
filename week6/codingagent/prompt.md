We want to make a coding agent which can solve simple bugs.
We will use the grok llm for this. see in the past files we will use thesame.

the llm will have some tools which will help in solving the bug.
One tool can be search files which lists path of files which are realated to the bug as per the llm.
we need searhc in file tool which can give line numbers reletaed to the bug
we need replace whilch allows the replacing a line with another line.

to test this, I wwant to test this mysefl. prepare a simple .cpp file and write boilerplate code in it. do not introduce any bug now,.
i will introduyce the bug and test it mysekf,

I want to give the bug in simple nenglish in cli and the llm and the tools should solvwe it.
meke the system without langgraph and keep it simple.
Also there will be max retry of 3 times. if the llm cant solve the bugs inside this limit it should print a message saying that it canot solve the bug/.

also there should be clear print statements saying whivch tool was calledat each steap[. we want to understand the flow completely.
as soon as i change the cpp file and run the agent it should ask me my buyg. after i give my bug, it should begin solving it.

do not write any test cases for now.
if anything is unclear, ask me.