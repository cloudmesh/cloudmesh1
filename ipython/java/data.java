import java.io.*;

class data {
    public static void main(String args[]){
        try{	     
	    File r = new File("data.csv");
	    FileWriter pw = new FileWriter(r);
	    PrintWriter pr = new PrintWriter(pw);
	    pr.println("x,y");
	    pr.println("0.1,1");
	    pr.println("1.2,2");
	    pr.println("2.3,1.5");
	    pr.close();
	} catch(IOException e) {}
    }
}