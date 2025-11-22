clear;
clc;

%% Load the data
load('cluedo2.mat');

%% Some initialization
nbChannels = size(EEG, 1);
nbSamples = size(EEG, 2);
nbTargets = 9;
suspectClasses = (11:19);
suspects = {'Brown', 'Mustard', 'Peach', 'Scarlett', 'Grey', 'Peacock', 'White', 'Plum', 'Green'};
weaponClasses = (21:29);
weapons = {'Axe', 'Blunderbuss', 'Candlestick', 'Dagger', 'Lead Pipe', 'Poison', 'Revolver', 'Rope', 'Spanner'};
locationClasses = (31:39);
locations = {'Ballroom', 'Billiard', 'Conservatory', 'Dining', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study'};

%% Get the onsets of the stimuli with corresponding class
onsets = find(markers);
classes = markers(onsets);

%% Cut the EEG into epochs
window = [-0.1, 1.0];
windowInSamples = fix(window * sampleRate);
nbSamplesInEpoch = numel(windowInSamples(1):windowInSamples(2));

% Find the samples to use for baselining
if window(1) < 0
    % only do baselining when you start cutting from pre-stimulus onset
    baselineSamples = (1 : -windowInSamples(1));
else
    % else, don't do baselining
    baselineSamples = [];
end

% Initialize the matrix where we will store the epochs
epochs = zeros(nbChannels, nbSamplesInEpoch, numel(onsets));
for o = 1 : numel(onsets)
    % Cut an epoch
    currentEpoch = EEG(:, onsets(o)+windowInSamples(1):onsets(o)+windowInSamples(2));
    %34x551

    % Baseline
    if ~isempty(baselineSamples)
        baseline = mean(currentEpoch(:,baselineSamples),2); %34x1
        currentEpoch = currentEpoch - repmat(baseline,1,nbSamplesInEpoch);
    end

    % Save the epoch in the matrix we made before
    epochs(:,:,o) = currentEpoch;
end

%% Select only the channels of interest
channelsOfInterest = {'Fz', 'Cz', 'CP1', 'CP2', 'Pz', 'PO3', 'PO4'};
channelIdc = zeros(1,numel(channelsOfInterest));
for ch = 1 : numel(channelsOfInterest)
    idx = find(ismember(channelNames, channelsOfInterest{ch}));
    assert(numel(idx) == 1);
    channelIdc(ch) = idx;
end
epochs = epochs(channelIdc, :, :);

%% Initialize plotting
colors = {[217,30,24]/255, [38,166,91]/255, [68,108,179]/255, [247,202,24]/255, [248,148,6]/255, [142,68,173]/255, [210,82,127]/255, [0,0,0]/255, [108,122,137]/255};
offset = repmat(((1:numel(channelIdc)) * 50)', [1, nbSamplesInEpoch]);
time = (windowInSamples(1):windowInSamples(2)) / sampleRate;

%% Plot!
figure;
for clue = 1 : 3
    if clue == 1
        current_classes = suspectClasses;
    elseif clue == 2
        current_classes = weaponClasses;
    else
        current_classes = locationClasses;
    end

    %% Average epochs per class
    averagedEpochs = zeros(size(epochs,1), size(epochs,2), numel(current_classes));
    for c = 1 : numel(current_classes)
        averagedEpochs(:,:,c) = mean(epochs(:,:,classes == current_classes(c)),3);
    end

    subplot(1,3,clue);
    hold on;
    ax = zeros(numel(channelIdc), numel(current_classes));
    for c = 1 : numel(current_classes)
        ax(:,c) = plot(time, (averagedEpochs(:,:,c) + offset)', 'Color', colors{c}, 'Linewidth',2);
    end
    set(gca, 'YTick', offset(:,1), 'YTickLabel', channelNames(channelIdc));
    set(gca, 'Color', [236 236 236]/255)
    xlim([-0.1, 1.0]);
    ylim([40, numel(channelIdc)*50+20])
    xlabel('Time (s)');
    ylabel('Channels');
    if clue == 1
        title('Suspects');
        legend(ax(1,:), suspects);
    elseif clue == 2
        title('Weapons');
        legend(ax(1,:),weapons);
    else
        title('Locations');
        legend(ax(1,:),locations);
    end
end
