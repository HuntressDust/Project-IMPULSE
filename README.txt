TO RUN IMPULSE:


The file Structure should be as follows

			Impulse V1121 Folder
		             		|
(impulse_v112.exe)		(GRAPHICS Folder)	(_internal Folder)
	                         | 				|
		         		........		 	.........

Run the EXE
__________________



This is a ASCII turn based RPG. Used [QWE ASD ZC ] or the NUMPAD to walk around one tile at a time and attack things.
To get to the next level, find the staircase marked with [>], you can use medbays marked with [X] to heal and install upgrades
The game ends when you die, or when you get bottom surgery at Floor 10
Press H to bring up the help screen with more info
V1.12, compiled 20-07-2026


Changelog
V1.121
You can no longer attack yourself
Increased cost of Drain, but increased its effectiveness. the idea is that you cant just wait around and siphon health from your allies and repair 
	them unless you have a lot of focus
Walls are now invalid targets for explosives. Before, your grenade would just be eaten and you'd loose your turn
Two handed weapons are now held in both hands when you equip it while unarmed
increased generation of flares and ammo, decreased Maids in the early game
Exterminators now wander like Maids
chasers now harass the player exclusively
you can now hack nano clouds. 


V1.12
Added more colors to messages for clarity
added dodge and accuracy calculations to melee attacks
ranged puppets now attack at range
puppets periodically may drain your fp slightly depending on the difference between your FOCUS and theirs
puppets now attempt to break free if your focus drops below theirs
rapiers now increase dodge instead of defense
the labrys now increases defense
fixed how elemental damage is calculated
shorted item info based on context
various balance tweaks

V1.1
Additions:
Added an explanation for how to used items in the help screen
added visual flair for the screen and some messages
enemies now breifly chase you after loosing sight of you
you can choose between a white or black '@' before starting
added the Maid, Chem-Slime, Nano Cloud, Aetheron enemies
addedmore information to enemy and item desctiptions
added destrciptions and mouse-over names to stairs and medbays
added rudimentary unarmed striking

changes:
The Labrys, Rapier, and hazmat PPe now have stat requirements, though they can still be used with reduced effectiveness
the sensors cyberware now reveals enemy locations instead of increasing FOV
combat dolls now try to self-destruct at low health
changed item, floor, wall, and enemy colors
many balance changes
you can swap places with all your puppets, not just dolls
weed gives the high status effect which protects against dysphoria for a time


Bugfixes:
Molotovs no longer break the game
The STATUS screen no longer breaks or shifts elements around if your reight hand is empty
repair.dll works as intended
added mouse support for ranged actions / looking
 "-corpse" no longer stacks on self-destructed dolls
5.57 rounds work as intended
attempting to use cyberware outside a medbay no longer raises an exception
you can no longer use the same medbay to install cyberware twice
ranged attacks more accuratlyu show whats out -of-range
rectified menu boxes so that text no longer sticks out
status effects no longer run into each other on the status screen
added checks to make sure most messages make gramatical sense
fixed many typos
you can no longer equip and unequip and reqeuip items in order to use 2 or even 3 two handed weapons
