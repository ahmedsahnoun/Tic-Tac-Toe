# Un etat est defini par une matrice 3x3 initialisée à 0
# le cadre pris par le joueur 1 prend la valeur 1
# le cadre pris par le joueur 2 prend la valeur 2

# cette fonction verifie si le jeu est terminé ou non
def gameover(etat):
   if not check_win(etat,1) and not check_win(etat,2):
      for i in range(3):
         for j in range(3):
            if etat[i,j] == 0:
               return(False)
   return(True)

# cette fonction retourne les etats fils
def child(etat,player):
   L = []
   for i in range(3):
      for j in range(3):
         if etat[i,j] == 0:
            temp = etat.copy()
            temp[i,j] = player
            L.append((temp,(i,j)))
   return(L)

def check_win(etat,player):
	# vertical win check
	for col in range(3):
		if etat[0][col] == player and etat[1][col] == player and etat[2][col] == player:
			return True

	# horizontal win check
	for row in range(3):
		if etat[row][0] == player and etat[row][1] == player and etat[row][2] == player:
			return True

	# asc diagonal win check
	if etat[2][0] == player and etat[1][1] == player and etat[0][2] == player:
		return True

	# desc diagonal win chek
	if etat[0][0] == player and etat[1][1] == player and etat[2][2] == player:
		return True

	return False

def H(etat,hauteur):
   if check_win(etat, 1):
      return(10+hauteur)
   if check_win(etat, 2):
      return(-10-hauteur)
   return(0)

# Les algorithmes suivants vont retourner (H(n),n,(x,y))
# H(n) est la valeur heuristique de l'etape suivante
# n est le nombre de noeuds parcouris
# (x,y) est la coordonnée que l'ia va choisir

def minimax(etat,hauteur,IsMaxPlayer):
   # nombre de noeuds dans le parcours
   n=0
   # la prochaine etape
   move = None

   if hauteur == 0 or gameover(etat):
      return (H(etat,hauteur),n,move)

   if IsMaxPlayer:
      # -20 est equivalent à -infini
      maxEval = -20
      # on evalue les fils de l'etat
      for fils in child(etat,1):
         calcul = minimax(fils[0], hauteur-1,False)
         # calcul[0] est l'evaluation d'etat
         evaluation = calcul[0]
         # calcul[1] est le nombre de noeud exploré a partir du fils
         n += calcul[1]+1
         if evaluation > maxEval:
            maxEval = evaluation
            # fils[1] est la case à cocher
            move = fils[1]
      return(maxEval,n,move)
   else:
      # 20 est equivalent à +infini
      minEval = 20
      for fils in child(etat,2):
      # on evalue les fils de l'etat
         calcul = minimax(fils[0], hauteur-1,True)
         # calcul[0] est l'evaluation d'etat
         evaluation = calcul[0]
         # calcul[1] est le nombre de noeud exploré a partir du fils
         n += calcul[1]+1
         if evaluation < minEval:
            minEval = evaluation
            # fils[1] est la case à cocher
            move = fils[1]
      return(minEval,n,move)

def AlphaBeta(etat,hauteur,alpha,beta,IsMaxPlayer):
   # nombre de noeuds dans le parcours
   n=0
   # la prochaine etape initalement inexistante
   move = None

   if hauteur == 0 or gameover(etat):
      return (H(etat,hauteur),n,None)

   if IsMaxPlayer:
      # on evalue les fils de l'etat
      for fils in child(etat,1):
         calcul = AlphaBeta(fils[0], hauteur-1,alpha,beta,False)
         # calcul[0] est l'evaluation d'etat
         evaluation = calcul[0]
         # calcul[1] est le nombre de noeud exploré a partir du fils
         n += calcul[1]+1
         if evaluation > alpha:
            alpha = evaluation
            # fils[1] est la case à cocher
            move = fils[1]
         # si beta <= alpha on ne cherche plus de fils
         if beta <= alpha:
            break
      return(alpha,n,move)
   else:
      # on evalue les fils de l'etat
      for fils in child(etat,2):
         calcul = AlphaBeta(fils[0], hauteur-1,alpha,beta,True)
         # calcul[0] est l'evaluation d'etat
         evaluation = calcul[0]
         # calcul[1] est le nombre de noeud exploré a partir du fils
         n += calcul[1]+1
         if evaluation < beta:
            beta = evaluation
            # fils[1] est la case à cocher
            move = fils[1]
         # si beta <= alpha on ne cherche plus de fils
         if beta <= alpha:
            break
      return(beta,n,move)