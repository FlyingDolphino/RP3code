clear; close all; clc; format short g; format compact;
set(0,'DefaultFigureWindowStyle','docked')
set(0,'defaultAxesFontSize',16)

% Open the results.txt file
fid = fopen('results.txt');




% Read the file line by line
tline = fgetl(fid);
i = 1;
iterationToPlot = [];
inputsToPlot = [];
objectiveToPlot = [];
minimum = [];

while ischar(tline)
    % Extract the iteration number, objective value and input values from each line
    iteration = str2double(regexp(tline, 'iteration = (\d+)', 'tokens', 'once'));
    objective = str2double(regexp(tline, 'objective = ([\d.]+)', 'tokens', 'once'));
    inputs_str = regexp(tline, 'inputs = \[(.*?)\]', 'tokens', 'once');
    inputs = str2num(inputs_str{1});
    
    if i ==1
        minimum(i) = objective;
    elseif objective < minimum(i-1);
        minimum(i) = objective;
    else
        minimum(i) = minimum(i-1);
    end
    
    
    iterationToPlot(i) = iteration;
    objectiveToPlot(i) = objective;
    inputsToPlot = [inputsToPlot;inputs];
    
    i = i+1;
    % Read the next line
    tline = fgetl(fid);
end

% Close the file
fclose(fid);
%plotting
%speed
hold on;
figure(1);
yyaxis right
plot(iterationToPlot,inputsToPlot(:,1),'LineStyle','-')
ylabel('Scaled and Normalized Speed Input');
yyaxis left
plot(iterationToPlot,minimum.*10,'LineWidth',1.5);
ylabel('Minimum Average RMS dBA');
grid on;
title('Speed against Average RMS dBA for Optimisation run');
xlabel('Iterations');


figure(2);
yyaxis right
plot(iterationToPlot,inputsToPlot(:,2),'LineStyle','-');
ylabel('Scaled and Normalized Descent Rate Input');
yyaxis left
plot(iterationToPlot,minimum.*10,'LineWidth',1.5);
grid on;
ylabel('Minimum Average RMS dBA');
title('Descent Rate against Average RMS dBA for Optimisation run');
xlabel('Iterations');

figure(3);
yyaxis right
plot(iterationToPlot,inputsToPlot(:,3),'LineStyle','-');
ylabel('Scaled and Normalized Hover Height Input');
yyaxis left
plot(iterationToPlot,minimum.*10,'LineWidth',1.5);
grid on;
ylabel('Minimum Average RMS dBA');
title('Hover Height against Average RMS dBA for Optimisation run');
xlabel('Iterations');

figure(4)
grid on;
yyaxis right
plot(iterationToPlot,inputsToPlot(:,4),'LineStyle','-');
ylabel('Scaled and Normalized Base Turn Input');
yyaxis left

plot(iterationToPlot,minimum.*10,'LineWidth',1.5);
title('Base Turn Course against Average RMS dBA for Optimisation run');
xlabel('Iterations');
ylabel('Minimum Average RMS dBA');


figure(5)
grid on;
yyaxis right
plot(iterationToPlot,inputsToPlot(:,5),'LineStyle','-');
ylabel('Scaled and Normalized Final Turn Input');
yyaxis left

plot(iterationToPlot,minimum.*10,'LineWidth',1.5);
title('Final Turn Course against Average RMS dBA for Optimisation run');
xlabel('Iterations');
ylabel('Minimum Average RMS dBA');


