### Basic Commands

- **clone** : Used to download the repository from GitHub.
    
    ```bash
    --syntax--
    $ git clone <url>
    
    --example
    $ git clone https://github.com/Latishfaction/test.git
    ```
    
- **add** : add the files which need to keep track of by GitHub.
    
    ```bash
    --syntax--
    $ git add <filename>
    
    --example--
    $ git add hello.html
    ```
    
    <aside>
    ❓ Why we use this command ? 
    ⇒ If we had 10 files and we need to keep track of only 3 or 2 files then we can add only the names of those **specific files .**
    
    </aside>
    
    - **commit** : to save a point after some amount of coding.
        
        ```bash
        --syntax--
        $ git commit -m "Message"
        
        --example--
        $ git commit -m "added some functionalities"
        ```
        
        <aside>
        📌 The commit message is going to reflected in all the files which we added in 
        **“$git add “** section
        
        </aside>
        
    
    ### In order to use add file on track and commit use
    
    Adds all the file on track to commit further
    
    ```bash
    -- syntax --
    $ git commit -am "Message"
    
    --example--
    $ git commit -am "Error at line 12 corrected✅"
    ```
    
- **push** : Transfers the code form our system to the main GitHub repository.
    
    ```bash
    -- syntax -- 
    $ git push
    
    --example--
    $ git push
    ```
    
    <aside>
    ⚠️ After being pushed we have to add { $ git add <filename> } file again in GitHub to keep track of change.
    
    ⇒ in order of avoid this used 
    
    $ git commit -am “Message”
    
    </aside>
    
- **status** : shows the status of our cloned repository (inside the system) and the main repository(in GitHub).
    
    ```bash
    --syntax--
    $ git status
    
    --example--
    $ git status
    ```
    
- **pull :** used to fetch the code from main GitHub’s repository.
    
    ```bash
    --syntax--
    $ git pull 
    
    --example--
    $ git pull
    ```
    
    <aside>
    ⚠️ If user different users try to change the same line then it will created merge conflict.
    While we make **pull**  request
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b2ba095d-a3c7-4068-b863-47b22378c36d/Untitled.png)
    
    **Merge Conflict
    <<<HEAD 
    {
    //code     ⇒ Changes done my local machine (on the same line)
    }**
    ==================================
    **{
    //code  ⇒ Changes done in GitHub version repo (on the same line)
    }**
    >>>>>>> #345345dbvfgry75764ftgg {hash}
    
    Conclusion : A developer have to merge the conflict manually.
    
    </aside>
    
- **log** : used to show the all commit information on the GitHub repo by local machine.
    
    ```bash
    -- syntax--
    $ git log
    ```
    

### Branching

- **branch** : shows all the branches and the current branch that we are operating on.
    
    ```bash
    $ git branch
    
    { branch name with prefix ***** specifies the current branch }
    ```
    
- **checkout** : create new branches or to go on particular branch.
    - **create new branch**
        
        ```bash
        -- syntax --
        $ git checkout -b <branch-name>
        
        -- example --
        $ git checkout -b css
        ```
        
    - **Jump to other branch**
        
        ```bash
        -- syntax --
        $ git checkout <branch-name>
        
        -- example --
        $ git checkout master
        ```
        
- **merge** : merges a branch to **a current branch.**
    
    ```bash
    -- syntax --
    $ git merge {branch-to-merge}
    
    -- example --
    $ git merge css
    ```
    
- **reset** : used to revert the changes back to **a particular commit** or **the current state of any branch**.
    
    ```bash
    -- syntax to change to **a particular commit** --
    $ git reset hard <commit-hash-id>
    
    -- syntax to change to a **current state of any branch --**
    $ git reset hard <branch>
    
    -- example to change to **a particular commit** --
    $ git reset hard #56y7fb
    
    -- example to change to a **current state of any branch --**
    $ git reset hard origin/master
    ```