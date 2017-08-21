% Title: mvbds.m
%
% Authors: Justin Jordan, David Ikemba, Thuong Nguyen, Woodrow Bogucki
% Date:  
% Project: Machine Vision Burr Detection System
%
% Sponsor: Hunt and Hunt Ltd.
% Faculty Advisor: Dr. Fred Chen
% Instructor: Dr. Compeau
% University: Texas State University Ingram School of Engineering
% 
% Description: The Machine Vision Burr Detection System (MVBDS) will
%    be designed by Texas State University Electrical Engineering
%    students, for Hunt and Hunt Ltd., to detect burrs at the
%    intersection of the keyway and inner-diameter threading of precision
%    machined pipes. The system will generate a pass/fail signal to let
%    the user know if burrs are detected. This is a proof of concept
%    design to demonstrate that machine vision can be used to automate
%    burr detection.
%    Minimum Requirements: The MVBDS must comply with the following:
%    Must detect defects within 1.5 minute time frame
%    Must generate pass/fail signal with 95% accuracy or greater
%    Must use Hunt & Hunt Ltd. Machined pipes
%    Must detect defects 1mm or larger
%    Project budget needs to be $500 or less

function main

% clears all variables and the console and closes all figures
clear;
clc;
close all;

% initialize the camera
% use webcam to take pictures, uncomment when using camera
% cam = webcam;
% preview(cam); 
% img = snapshot(cam);
% img = rgb2gray(img); % convert to grayscale
% create new figure

FIG = figure( 'Name','MVBDS','CloseRequestFcn',@exitProgram, ...
    'NumberTitle','off', 'Units', 'Pixels',  ...
    'Position', [100 100 850 700], 'Visible','on');

% creates axes for a preview image window
preview = axes('Parent', FIG, 'Units', 'Pixels', ...
    'Position', [25 25 800 600]);

% creates a panel to group the controls together
panel = uipanel('Parent', FIG, 'Units', 'Pixels',...
    'Title', 'Control Panel', 'Position', [30 640 790 60]);

% creates a start/stop preview button
openImg = uicontrol('Parent', panel, 'Units', 'Normalized', ...
    'String', 'Open Image', 'Position', [0.025 0.2 0.2 0.6], ...
    'Callback', @openImage);

% creates a capture image button
testing = uicontrol('Parent', panel, 'Units', 'Normalized', ...
    'String', 'Begin Test', 'Position', [0.25 0.2 0.2 0.6], ...
    'Callback', @beginTest);

% global variables to be used throughout program
exitProg = 0;
img = [];


% create detector, thread_end_side_fa_05_numStages_10_haar.xml
detector = vision.CascadeObjectDetector(...
    'thread_end_side_fa_0475_numStages_10_haar.xml', 'MaxSize', ...
    [210 140], 'MinSize', [150 100], 'MergeThreshold', 160, ...
    'UseROI', true); % thread_end_side_fa_05_numStages_10_haar.xml
       
    function [retImg] = passMsg(img)
    % This function returns the input img with an added pass inidication
        position = [size(img,2)/2, size(img,1)/2];
        retImg = insertText(img, position, 'Pass', 'FontSize', 80, ...
            'BoxColor', 'green', 'BoxOpacity', 0.6, 'TextColor', 'white');
    end
    
    function [retImg] = failMsg(img)
    % This function returns the input img with an added fail indication
        position = [size(img,2)/2, size(img,1)/2];
        retImg = insertText(img, position, 'Fail', 'FontSize', 80, ...
            'BoxColor', 'red', 'BoxOpacity', 0.6, 'TextColor', 'white');
    end

    function beginTest(hObject, eventdata, handles)
    % This function runs through test of img and 
    % generates pass/fail indication
        axes(preview);
        ROI = imrect(gca);
        roi = uint16(wait(ROI));
        
        % take adaptive histogram of image
        imgHist = adapthisteq(img);

        % detect thread ends in keyway ROI
        bbox = step(detector, imgHist, roi);

        % create image showing detections
        detectedImg = insertObjectAnnotation(img, 'rectangle', bbox, ...
            'thread_end');

        % determine pass/fail status
        if size(bbox, 1) == 4
            detectedImg = passMsg(detectedImg);
        else
            detectedImg = failMsg(detectedImg);
        end
        
        % show results of burr detection with pass/fail status
        axes(preview);
        imshow(detectedImg)
    end

    function openImage(hObject, eventdata, handles)
    % this function opens an image using uigetfile. 
    % a window allows user to select any image filetype.
        currentDir=cd;
        
        [file, path] = uigetfile({...
        '*.png','PNG (*.png)';...
        '*.*','All files (*.*)'});
        
        if path == 0
            disp('User cancelled');
            return;
        end
        
        cd(path);
        img = imread(file);
        cd(currentDir);
        
        axes(preview);
        imshow(img);
    end

    function exitProgram(src, callbackdata)
    % This exits the program when the figure is closed
        exitProg = 1;
        clear('cam');
        delete(FIG)
        return 
    end
end