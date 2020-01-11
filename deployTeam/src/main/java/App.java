import java.util.Scanner;

public class App {

    public static void main(String[] args) {

        System.out.println("Hello from deploy team");

        Scanner input = new Scanner(System.in);

        System.out.print("Enter an integer: ");
        int firstInt = input.nextInt();

        System.out.print("Enter another integer: ");
        int secInt = input.nextInt();


        System.out.println("Sum is : " + (firstInt+secInt));

    }

}
