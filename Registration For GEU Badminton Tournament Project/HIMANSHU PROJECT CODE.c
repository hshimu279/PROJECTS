#include<stdio.h>
int main(){
  
  int ch=4,m=0,f=0;
  struct player_details{
    char name[20];
    int age;
    char gender;
    int entry_type;
    int amt;
  }player_details;

  struct sponsor{
    char name[20];
    float amt;
    int lvl;
  }sponsor;
  
  player_details.amt = 0;
  while(ch!=3){
    printf("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n");
    printf("      GEU BADMINTON TOURNAMENT     \n");
    printf("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n");
    printf("1. Player login\n");
    printf("2. Sponsor login\n");
    printf("3. EXIT\n");
    printf("Enter your choice to continue: ");
    scanf("%d",&ch);

printf("\n");
  //1.Player's Login:
    if(ch==1){
      printf("°~°~°~°~°~°~°~°~°~°~°~°~°`°~°~°~°~°~°\n");
      printf("      GEU BADMINTON TOURNAMENT     \n");
      printf("--------WELCOME DEAR PLAYERS-------\n");
      printf("°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°~°\n");

      //Entry type:
      printf("1. Single entry\n");
      printf("2. Double entry\n");
      printf("3. Mixed entry\n");
      printf("Choose the entry type: \n");
      scanf("%d",&player_details.entry_type);

      int i=0;
      if(player_details.entry_type==1){
        i=2;
      }
      else if(player_details.entry_type==2 || player_details.entry_type==3){
        i=3;
      }

      for(int j=1;j<i;j++){
        player_details.age = 20;
        printf("\n-----------------------------------\n");
        printf("Enter your name of player %d: ",j);
        scanf("%s",&player_details.name);
        printf("Player's age must be between 18y/o to 25y/o\n");
        while(player_details.age>18 && player_details.age<25){
          printf("Enter your age of player %d: ",j);
          scanf("%d",&player_details.age);
          if(player_details.age<18){
            printf("Player's age must be greater than 18y/o");
          }
          else if(player_details.age>25){
            printf("Player's age must be less than 25y/o");
          }
          else{
            break;
          }
        }
        while(m!=15 && f!=15){
          printf("Enter your gender(M/F) of player %d: ",j);
          scanf("%s",&player_details.gender);
          if(player_details.gender == 'm' || player_details.gender == 'M'){
            if(m<15){
              m++;
            }
            else{
              break;
            }
          }
          else if(player_details.gender == 'f' || player_details.gender == 'F'){
            if(f<15){
              f++;
            }
            else{
              break;
            }
          }
          printf("Male: %d, Female: %d \n",m,f);
          printf("\n");
          break;
        }


        //Payment Gateway:
      
        while(player_details.amt!=250){
          printf("-----------------------------------\n");
          printf("Enter the entry amount (i.e. Rs.250): ");  
          scanf("%d",&player_details.amt);
          printf("-----------------------------------\n");

          if(player_details.amt>250){
            printf("Enter the lesser amount(i.e. Rs.250)!!!\n\n");
          }
          else if(player_details.amt<250){
            printf("Enter the higher amount(i.e. Rs.250)!!!\n\n");
          }
          else if(player_details.amt==250){
            printf("player_details.amt completed sucessfully!!!\n");
            printf("Visit www.geubadminton.com to upload Fitness and age documents!!!\n");
          }
        }
      } 
    }

  // Sponsor:
    else if(ch==2){
      printf("-----------------------------------\n");
      printf("      GEU BADMINTON TOURNAMENT     \n");
      printf("WELCOME DEAR SPONSERS   ✺◟( ͡° ͜ʖ ͡°)◞✺\n");
      printf("-----------------------------------\n");
      printf("Enter the name of sponsor: ");
      scanf("%s",&sponsor.name);
      printf("Enter the amount for sponsor: ");
      scanf("%f",&sponsor.amt);
      printf("\n");
      printf("1. Silver Level - Banner at main gate\n");
      printf("2. Golden Level - Logo on game tshirts\n");
      printf("3. Platinum Level - Both the above mentioned facilities\n");
      printf("Enter the level of sponsor: ");
      scanf("%d",&sponsor.lvl);

      float pos1=0.15*sponsor.amt, pos2=0.075*sponsor.amt, pos3=0.025*sponsor.amt;
      printf("Prize for Singles:\n");
      printf("Prize for 1st Position: %f\n",pos1);
      printf("Prize for 2nd Position: %f\n",pos2);
      printf("Prize for 3rd Position: %f\n",pos3);
      printf("SAME PRIZES WILL BE DISTRIBUTED FOR DOUBLES AND MIXED PLAYERS\n");
    }
  }
  printf("-----------------------------------\n");
  printf("THERE ARE 10 BADMINTON COURTS AVAILABLE IF YOU HAVE ENROLLED IN TOURNAMENT YOU WILL GET NOTIFIED ON YOUR PHONE BY MESSAGE\n");
  printf("-----------------------------------\n");
  printf("      GEU BADMINTON TOURNAMENT     \n");
  printf("-----------------------------------\n");
  printf("-------THANKS FOR VISITING-------\n");
  printf("-----------------------------------\n");
  return 0;
}