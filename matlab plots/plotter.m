close all;
clear all;

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
plot(iterationToPlot,inputsToPlot(:,1),'r')
plot(iterationToPlot,inputsToPlot(:,2),'g');
plot(iterationToPlot,inputsToPlot(:,3),'b');
yyaxis left
plot(iterationToPlot,minimum);







