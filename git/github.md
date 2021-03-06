# Github

In diesem Dokument sammel ich Dinge, die explizit mit **github** zusammenhängen (nicht nur **git**).

## SSH Key für Github
1. Check, ob schon ein ssh-Schlüssel existiert:
   ~~~ bash
   // Git Bash
   $ ls -al ~/.ssh
   ~~~
   Schaue, ob eine Datei
   * `id_rsa.pub`
   * `id_ecdsa.pub`
   * `id_ed25519.pub`
   
   existiert.
2. Wenn keiner existiert, erstelle einen neuen:
   1. öffne eine Bash (z.B. Git Bash)
   2. Erzeuge einen Schlüssel mit der gegebenen email als Label
        ~~~ bash
      // Git Bash
      $ ssh-keygen -t ed25519 -C "<your_email@example.com>"
      ~~~
   3. In der öffnenden Maske gib einen *passphase* ein
3. Für den Auto-Start von `ssh-agent` für Git für Windows füge in der Git shell in die Datei `~/.profile`
   ein: (man kann dann auch den Schlüssel das WSL-Homes kopieren und folgendes auch dort in die .profile)
   ~~~ bash
   env=~/.ssh/agent.env

   agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

   agent_start () {
      (umask 077; ssh-agent >| "$env")
      . "$env" >| /dev/null ; }

   agent_load_env

   # agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2=agent not running
   agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

   if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
      agent_start
      ssh-add
   elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
      ssh-add
   fi

   unset env
   ~~~
4. Füge den SSH Schlüssel dem GitHub-Account hinzu
   1. Kopiere den *public key* ins Clipboard
      ~~~ bash
      // Git Bash
      $ clip < ~/.ssh/id_ed25519.pub
      ~~~
   2. In GitHub (webbrowser) öffne **Settings**
      
      ![settings](./settings.png)
   3. Unter **Access** wähle **SSH and GPG keys**
      ![a](./access_ssh.png)
   4. Wähle **New SSH key**
   5. Gib einen sinnvollen Titel ein, z.B. *JensRM bei INIT Software*
   6. Paste den kopierten Schlüssel in das dafür vorgesehene Feld ein
   7. Schließe ab mit **Add SSH key**
   8. Gib das GitHub-Passwort ein
      
## GitHub Verknüpfe lokales Repo mit GitHub Repo
1. Verknüpfen (benutze am besten die "Kopiervorlage" von GitHub)
   ~~~ bash
   // Git Bash
   $ git remote add <my_name_for_remote_repo> git@github.com:<portfolio>/<repo>.git
   ~~~
   Häufig ist der Wert für *my_name_for_remote_repo*, **origin**.

   Zur Kontrolle: `$ git remote -v`
2. Gib an, wie der zugehörige Branch auf dem Remote Repo heißt und pushe dahin.
   Dies wird vermutlich nicht funktionieren!
   ~~~ bash
   $ git push --set-upstream <my_name_for_remote_repo> origin master
   ~~~
3. Korrektur
   1. Hole den Branch vom remote repo
      ~~~ bash
      $ git fetch <my_name_for_remote_repo> <remote_branch>
      ~~~
      Typischerweise `git fetch origin master`, im Folgenden nehme ich einfach origin und master.
   2. Dann muss die Geschichte von `origin/master` mit der des lokalen Branches verknüpft werden
      ~~~ bash
      $ git merge origin/master --allow-unrelated-histories
      ~~~
   3. Höchstwahrscheinlich gibt es Probleme beim Mergen, die müssen dann manuell behoben werden
      und anschließend per `git add ...` hinzugefügt werden.
   4. Um den Merge abzuschließen ist dann ein
      ~~~ bash
      $ git commit
      ~~~
      nötig.
   5. Nun lässt sich das Pushen auf den "upstream" wiederholen
      ~~~ bash
      $ git push --set-upstream origin master
      ~~~


## Token für Github benutzen

## Github Desktop und CLI